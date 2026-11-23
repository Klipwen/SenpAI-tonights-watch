import streamlit as st
from pathlib import Path

from config import (
    APP_TITLE,
    APP_SUBTITLE,
    APP_ICON,
    ASSET_PATHS,
    get_api_key
)
from ui.styles import inject_custom_styles
from ui.components import render_sidebar, render_anime_card
from core.llm_client import generate_senpai_response

# 1. Page Configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON if APP_ICON and Path(APP_ICON).exists() else None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject Custom Theme Styles
inject_custom_styles(ASSET_PATHS["background"])

# 3. Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hi! I am SenpAI, your anime recommendation buddy. "
                "Use the quiz on the left sidebar for quick targeted picks, "
                "or tell me directly in chat how you are feeling and how much time you have tonight."
            ),
            "cards": []
        }
    ]

if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

# 4. Action Handlers (Callbacks for Quiz & Card Actions)
def handle_quiz_submit(quiz_data):
    """Formats quiz answers into a natural chat request."""
    genres_str = ", ".join(quiz_data["genres"]) if quiz_data["genres"] else "Any"
    favorite_str = f" My favorite anime is {quiz_data['favorite']}." if quiz_data["favorite"] else ""
    prompt = (
        f"I am looking for recommendations. "
        f"My current mood is '{quiz_data['mood']}' and I have '{quiz_data['time']}' available tonight. "
        f"Preferred genres: {genres_str}.{favorite_str} "
        f"Please recommend 3 spoiler-free titles matching this."
    )
    st.session_state.pending_prompt = prompt

def handle_card_action(action_type: str, anime_title: str):
    """Handles 'Compare This' or 'More Like This' card clicks."""
    if action_type == "compare":
        prompt = f"Can you compare '{anime_title}' with another similar anime in terms of tone, length, and pacing to help me decide?"
    elif action_type == "similar":
        prompt = f"I really like '{anime_title}'. Can you suggest 3 titles similar to it with reasons why?"
    else:
        prompt = f"Tell me more about '{anime_title}'."
    st.session_state.pending_prompt = prompt
    st.rerun()

# 5. Render Sidebar
sidebar_data = render_sidebar(on_quiz_submit=handle_quiz_submit)

# 6. Main Header
st.markdown(f'<div class="app-header-title">{APP_TITLE}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="app-header-subtitle">{APP_SUBTITLE}</div>', unsafe_allow_html=True)

# 7. Render Chat History
senpai_avatar = str(ASSET_PATHS["senpai_avatar"]) if ASSET_PATHS["senpai_avatar"].exists() else None
user_avatar = str(ASSET_PATHS["user_avatar"]) if ASSET_PATHS["user_avatar"].exists() else None

for msg_idx, msg in enumerate(st.session_state.messages):
    avatar = senpai_avatar if msg["role"] == "assistant" else user_avatar
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        
        # Render enriched anime cards if present
        cards = msg.get("cards", [])
        if cards:
            st.divider()
            for rank, anime in enumerate(cards, 1):
                render_anime_card(anime, rank=rank, on_action=handle_card_action)

# 8. Handle Input (From Chat Box or Pending Quiz/Card Prompts)
user_input = st.chat_input("Ask SenpAI for recommendations, comparisons, or titles like your favorite...")

prompt_to_send = None
if st.session_state.pending_prompt:
    prompt_to_send = st.session_state.pending_prompt
    st.session_state.pending_prompt = None
elif user_input:
    prompt_to_send = user_input

if prompt_to_send:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt_to_send, "cards": []})
    
    with st.chat_message("user", avatar=user_avatar):
        st.markdown(prompt_to_send)

    # Process response with SenpAI
    with st.chat_message("assistant", avatar=senpai_avatar):
        # Optional Chibi loading visual
        if ASSET_PATHS["loading_chibi"].exists():
            loading_placeholder = st.empty()
            with loading_placeholder.container():
                st.image(str(ASSET_PATHS["loading_chibi"]), width=120)
                st.caption("SenpAI is searching verified anime data...")
        else:
            loading_placeholder = st.empty()
            loading_placeholder.info("SenpAI is evaluating your mood and time budget...")

        api_key = get_api_key()
        response_text, enriched_cards = generate_senpai_response(
            api_key=api_key,
            user_message=prompt_to_send,
            chat_history=st.session_state.messages[:-1],
            mood=sidebar_data["mood"],
            time_budget=sidebar_data["time"],
            spoiler_free=sidebar_data["spoiler_free"],
            content_rating=sidebar_data["rating"],
            model_name=sidebar_data["model"]
        )

        loading_placeholder.empty()
        st.markdown(response_text)

        if enriched_cards:
            st.divider()
            for rank, anime in enumerate(enriched_cards, 1):
                render_anime_card(anime, rank=rank, on_action=handle_card_action)

    # Save assistant message to session state
    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text,
        "cards": enriched_cards
    })
    st.rerun()
