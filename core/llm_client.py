import logging
import re
from typing import List, Dict, Any, Optional, Tuple
from google import genai
from google.genai import types

from core.prompt_manager import get_system_prompt
from core.guardrails import check_prompt_injection, apply_sandwich_defense
from core.tools import search_anime

logger = logging.getLogger(__name__)

def parse_recommended_titles(text: str) -> List[str]:
    """
    Extracts recommended anime titles from the assistant output text.
    Matches lines like: '1. **Title**' or '1. Title (episodes)'
    """
    titles = []
    # Pattern 1: Bolded titles: 1. **Title**
    matches = re.findall(r"^\s*\d+\.\s+\*\*([^*]+)\*\*", text, flags=re.MULTILINE)
    if matches:
        for m in matches:
            clean = m.strip()
            if clean and clean not in titles:
                titles.append(clean)
    else:
        # Pattern 2: Non-bolded: 1. Title (episodes)
        matches2 = re.findall(r"^\s*\d+\.\s+([^(:\n\-]+)", text, flags=re.MULTILINE)
        for m in matches2:
            clean = m.strip()
            if clean and clean not in titles:
                titles.append(clean)
    return titles[:5]

def generate_senpai_response(
    api_key: str,
    user_message: str,
    chat_history: List[Dict[str, str]],
    mood: str = "",
    time_budget: str = "",
    spoiler_free: bool = True,
    content_rating: str = "Teens (PG-13)",
    model_name: str = "gemini-2.5-flash"
) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Main orchestration function for SenpAI:
    1. Guardrail validation (pre-flight check).
    2. Sandwich defense & XML encapsulation.
    3. Multi-turn conversation assembly.
    4. Gemini API invocation.
    5. Automatic poster & metadata enrichment via Jikan tool.
    """
    # Step 1: Pre-flight Guardrail Filter (Defense 1)
    is_safe, refusal_reason = check_prompt_injection(user_message)
    if not is_safe:
        return refusal_reason, []

    if not api_key:
        return (
            "Gemini API key is not configured. Please add your GEMINI_API_KEY to "
            ".streamlit/secrets.toml or your environment variables to continue.",
            []
        )

    # Step 2: Apply Sandwich Defense & XML Encapsulation (Defenses 2 & 3)
    defensive_prompt = apply_sandwich_defense(
        user_input=user_message,
        mood=mood,
        time_budget=time_budget,
        spoiler_free=spoiler_free,
        content_rating=content_rating
    )

    try:
        client = genai.Client(api_key=api_key)

        # Assemble conversation history into Gemini format
        contents = []
        for msg in chat_history[-6:]:  # Keep recent context window concise
            role = "user" if msg["role"] == "user" else "model"
            contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=msg["content"])]
                )
            )

        # Append current defensive user prompt
        contents.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=defensive_prompt)]
            )
        )

        # Generate response using system instruction and temperature
        config = types.GenerateContentConfig(
            system_instruction=get_system_prompt(),
            temperature=0.7,
            max_output_tokens=1000,
        )

        # Resilient Model Fallback Chain (handles temporary 503 server demand spikes)
        candidate_models = [model_name]
        for fallback in ["gemini-3.5-flash-lite", "gemini-3.8-flash", "gemini-3.5-flash"]:
            if fallback not in candidate_models:
                candidate_models.append(fallback)

        response = None
        last_error = None
        for candidate in candidate_models:
            try:
                response = client.models.generate_content(
                    model=candidate,
                    contents=contents,
                    config=config
                )
                if response and response.text:
                    break
            except Exception as candidate_err:
                last_error = candidate_err
                logger.warning(f"Candidate model {candidate} returned error: {candidate_err}. Trying next fallback...")

        if not response or not response.text:
            if last_error:
                raise last_error
            return "I could not generate a recommendation right now. Please try again.", []

        response_text = response.text

        # Step 3: Agentic Enrichment - Extract titles and fetch verified Jikan metadata & posters
        recommended_titles = parse_recommended_titles(response_text)
        enriched_anime = []
        for title in recommended_titles:
            jikan_results = search_anime(title, limit=1)
            if jikan_results:
                enriched_anime.append(jikan_results[0])

        return response_text, enriched_anime

    except Exception as e:
        logger.error(f"Error calling Gemini API: {e}")
        return f"Encountered an issue connecting to the AI service: {str(e)}", []
