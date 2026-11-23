import os
from pathlib import Path
import streamlit as st

# Base Directory & Paths
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

ASSET_PATHS = {
    "favicon": ASSETS_DIR / "favicon.png",
    "banner": ASSETS_DIR / "banner.png",
    "senpai_avatar": ASSETS_DIR / "senpai_avatar.png",
    "user_avatar": ASSETS_DIR / "user_avatar.png",
    "loading_chibi": ASSETS_DIR / "loading_chibi.gif",
    "empty_watchlist": ASSETS_DIR / "empty_watchlist.png",
    "background": ASSETS_DIR / "background.jpg",
}

# App Branding & Meta
APP_TITLE = "SenpAI: Tonight's Watch"
APP_SUBTITLE = "Personalized anime recommender tailored to your mood and available time."
APP_ICON = str(ASSET_PATHS["favicon"]) if ASSET_PATHS["favicon"].exists() else None

# AI Model Defaults
DEFAULT_MODEL = "gemini-3.5-flash"
AVAILABLE_MODELS = ["gemini-3.5-flash", "gemini-3.5-flash-lite", "gemini-3.8-flash"]
DEFAULT_TEMPERATURE = 0.7

# Preset Taxonomy for Quiz
MOOD_OPTIONS = [
    "Select your mood...",
    "Chill & Cozy",
    "Hyped & Energetic",
    "Sad / In Need of Hope",
    "Curious & Thoughtful",
    "Romantic & Sweet",
    "Dark & Thrilling",
    "Melodic & Classical Music Lovers",
]

GENRE_OPTIONS = [
    "Action", "Adventure", "Comedy", "Drama", "Fantasy",
    "Music", "Mystery", "Romance", "Sci-Fi", "Slice of Life",
    "Sports", "Supernatural", "Suspense", "Psychological"
]

RATING_OPTIONS = [
    "All Ages (G)",
    "Teens (PG-13)",
    "Mature (R17+)"
]

TIME_BUDGETS = {
    "1 Episode (~25 mins)": 25,
    "2-3 Episodes (~1 hour)": 60,
    "Full Movie (~2 hours)": 120,
    "Short Series / OVA (~4 hours)": 240,
    "Weekend Marathon (12+ hours)": 720
}

def get_api_key() -> str:
    """
    Safely retrieves the Gemini API key from Streamlit secrets,
    environment variables, or local .env file.
    """
    # 1. Check Streamlit Secrets (for Streamlit Community Cloud)
    try:
        if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"]:
            return st.secrets["GEMINI_API_KEY"].strip()
    except Exception:
        pass

    # 2. Check Environment Variables
    env_key = os.getenv("GEMINI_API_KEY")
    if env_key:
        return env_key.strip()

    # 3. Check local .env file if python-dotenv is present
    try:
        from dotenv import load_dotenv
        load_dotenv(BASE_DIR / ".env")
        local_key = os.getenv("GEMINI_API_KEY")
        if local_key:
            return local_key.strip()
    except Exception:
        pass

    return ""
