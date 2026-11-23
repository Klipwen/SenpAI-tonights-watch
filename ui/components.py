import json
from pathlib import Path
from typing import Dict, Any, List, Callable
import streamlit as st

from config import (
    ASSET_PATHS,
    MOOD_OPTIONS,
    GENRE_OPTIONS,
    RATING_OPTIONS,
    TIME_BUDGETS,
    DEFAULT_MODEL,
    AVAILABLE_MODELS,
    DEFAULT_TEMPERATURE,
)

def render_sidebar(on_quiz_submit: Callable[[Dict[str, Any]], None]) -> Dict[str, Any]:
    """
    Renders the sidebar containing:
    1. Visual Banner
    2. Tonight's Watch Quiz Form
    3. Session Watchlist with Clear & Export
    4. Advanced Controls (Model switcher & prompt defense indicator)
    """
    with st.sidebar:
        # 1. Banner
        if ASSET_PATHS["banner"].exists():
            st.image(str(ASSET_PATHS["banner"]), use_container_width=True)

        st.markdown("### Tonight's Watch Quiz")
        st.caption("Tell SenpAI what you are in the mood for.")

        # 2. Quiz Controls
        selected_mood = st.selectbox("Mood", options=MOOD_OPTIONS, index=0)
        
        selected_time = st.select_slider(
            "Time Available",
            options=list(TIME_BUDGETS.keys()),
            value="Full Movie (~2 hours)"
        )

        favorite_anime = st.text_input(
            "Favorite Anime (Optional)",
            placeholder="e.g. Your Lie in April, Frieren"
        )

        selected_genres = st.multiselect(
            "Genres",
            options=GENRE_OPTIONS,
            default=[]
        )

        selected_rating = st.selectbox(
            "Content Rating",
            options=RATING_OPTIONS,
            index=1
        )

        spoiler_free = st.checkbox("Spoiler-free mode", value=True)

        quiz_clicked = st.button("Get Recommendations", use_container_width=True, type="primary")
        if quiz_clicked:
            on_quiz_submit({
                "mood": selected_mood,
                "time": selected_time,
                "favorite": favorite_anime,
                "genres": selected_genres,
                "rating": selected_rating,
                "spoiler_free": spoiler_free
            })

        st.divider()

        # 3. Watchlist Section
        render_watchlist_section()

        st.divider()

        # 4. Settings & Rubric Defense Status
        with st.expander("System Settings & Defenses", expanded=False):
            st.markdown(
                '<span class="defense-active-pill">DEFENSES ACTIVE</span>',
                unsafe_allow_html=True
            )
            st.caption("XML Encapsulation + Pre-flight Filter + Sandwich Defense enabled.")
            
            chosen_model = st.selectbox(
                "Model",
                options=AVAILABLE_MODELS,
                index=0
            )
            chosen_temp = st.slider("Temperature", min_value=0.0, max_value=1.0, value=DEFAULT_TEMPERATURE, step=0.05)

    return {
        "mood": selected_mood,
        "time": selected_time,
        "favorite": favorite_anime,
        "genres": selected_genres,
        "rating": selected_rating,
        "spoiler_free": spoiler_free,
        "model": chosen_model,
        "temperature": chosen_temp
    }

def render_watchlist_section():
    """Renders the user's active session watchlist."""
    st.markdown("### Watchlist")
    watchlist = st.session_state.get("watchlist", [])

    if not watchlist:
        if ASSET_PATHS["empty_watchlist"].exists():
            st.image(str(ASSET_PATHS["empty_watchlist"]), width=140)
        st.caption("No anime added yet. Click 'Add to Watchlist' on any recommendation.")
    else:
        st.markdown('<div class="watchlist-box">', unsafe_allow_html=True)
        for idx, title in enumerate(watchlist, 1):
            cols = st.columns([0.85, 0.15])
            with cols[0]:
                st.markdown(f'<div class="watchlist-item"><strong>{idx}.</strong> {title}</div>', unsafe_allow_html=True)
            with cols[1]:
                if st.button("X", key=f"del_wl_{idx}_{title}", help="Remove from watchlist"):
                    st.session_state.watchlist.remove(title)
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Clear All", use_container_width=True):
                st.session_state.watchlist = []
                st.rerun()
        with col2:
            export_data = "\n".join([f"{i+1}. {t}" for i, t in enumerate(watchlist)])
            st.download_button(
                label="Export",
                data=export_data,
                file_name="senpai_watchlist.txt",
                mime="text/plain",
                use_container_width=True
            )

def render_anime_card(anime: Dict[str, Any], rank: int, on_action: Callable[[str, str], None]):
    """
    Renders a rich anime card enriched by Jikan API data.
    Strictly follows the zero-emoji requirement.
    """
    with st.container():
        cols = st.columns([0.22, 0.78])
        with cols[0]:
            if anime.get("image_url"):
                st.image(anime["image_url"], use_container_width=True)
            else:
                st.caption("No Cover Available")
        
        with cols[1]:
            st.markdown(f'<span class="anime-rank-pill">PICK {rank}</span>', unsafe_allow_html=True)
            title = anime.get("title_english") or anime.get("title", "Unknown Title")
            st.markdown(f'<div class="anime-title-text">{title}</div>', unsafe_allow_html=True)
            
            # Metadata pills
            episodes = f"{anime.get('episodes')} eps" if anime.get("episodes") != "Unknown" else anime.get("duration", "")
            score = f"Score: {anime.get('score')}"
            rating = anime.get("rating", "")
            st.markdown(
                f'<span class="anime-meta-tag">{episodes}</span> | '
                f'<span class="anime-meta-tag">{score}</span> | '
                f'<span class="anime-meta-tag">{rating}</span>',
                unsafe_allow_html=True
            )
            
            synopsis = anime.get("synopsis", "")
            if synopsis:
                st.markdown(f'<div class="anime-synopsis-text">{synopsis}</div>', unsafe_allow_html=True)

            # Action Buttons
            btn_col1, btn_col2, btn_col3 = st.columns(3)
            with btn_col1:
                if st.button("Add to Watchlist", key=f"add_wl_{rank}_{anime.get('mal_id')}"):
                    if title not in st.session_state.watchlist:
                        st.session_state.watchlist.append(title)
                        st.toast(f"Added {title} to your watchlist.")
                        st.rerun()
            with btn_col2:
                if st.button("Compare This", key=f"cmp_{rank}_{anime.get('mal_id')}"):
                    on_action("compare", title)
            with btn_col3:
                if st.button("More Like This", key=f"more_{rank}_{anime.get('mal_id')}"):
                    on_action("similar", title)
