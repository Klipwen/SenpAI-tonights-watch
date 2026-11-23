import base64
from pathlib import Path
import streamlit as st

def get_image_base64(path: Path) -> str:
    """Helper to convert local image to base64 string for CSS embedding."""
    if path.exists():
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

def inject_custom_styles(background_path: Path):
    """
    Injects human-crafted, professional CSS styles.
    Enforces the zero-emoji requirement and applies subtle branding.
    """
    bg_css = ""
    if background_path.exists():
        b64_bg = get_image_base64(background_path)
        bg_css = f"""
        .stApp {{
            background: linear-gradient(180deg, rgba(15, 17, 23, 0.94) 0%, rgba(15, 17, 23, 0.98) 100%),
                        url("data:image/jpeg;base64,{b64_bg}") center / cover fixed no-repeat;
        }}
        """

    css = f"""
    <style>
    {bg_css}

    /* Clean typography */
    html, body, [class*="css"] {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}

    /* Header styling */
    .app-header-title {{
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        color: #F8F9FA;
        margin-bottom: 0.2rem;
    }}

    .app-header-subtitle {{
        font-size: 1rem;
        font-weight: 400;
        color: #ADB5BD;
        margin-bottom: 1.5rem;
    }}

    /* Card styling for anime recommendation items */
    .anime-card {{
        background-color: #1A1D24;
        border: 1px solid #2B303C;
        border-radius: 8px;
        padding: 1rem;
        margin-top: 0.8rem;
        margin-bottom: 0.8rem;
        display: flex;
        flex-direction: row;
        gap: 1.2rem;
        align-items: flex-start;
    }}

    .anime-card-poster {{
        width: 90px;
        height: 125px;
        object-fit: cover;
        border-radius: 6px;
        border: 1px solid #343A46;
        flex-shrink: 0;
    }}

    .anime-card-body {{
        flex-grow: 1;
    }}

    .anime-rank-pill {{
        display: inline-block;
        background-color: #E63946;
        color: #FFFFFF;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 4px;
        margin-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    .anime-title-text {{
        font-size: 1.15rem;
        font-weight: 600;
        color: #FFFFFF;
        margin: 0 0 4px 0;
    }}

    .anime-meta-tag {{
        display: inline-block;
        font-size: 0.8rem;
        color: #9097A3;
        margin-right: 10px;
    }}

    .anime-synopsis-text {{
        font-size: 0.85rem;
        color: #CED4DA;
        line-height: 1.4;
        margin-top: 6px;
    }}

    /* Sidebar adjustments */
    section[data-testid="stSidebar"] {{
        background-color: #14171E;
        border-right: 1px solid #232731;
    }}

    /* Watchlist styling */
    .watchlist-box {{
        background-color: #1B1F27;
        border: 1px solid #2A303D;
        border-radius: 6px;
        padding: 0.8rem;
        margin-top: 0.5rem;
        margin-bottom: 0.8rem;
    }}

    .watchlist-item {{
        font-size: 0.9rem;
        color: #E9ECEF;
        padding: 4px 0;
        border-bottom: 1px solid #242935;
    }}

    .watchlist-item:last-child {{
        border-bottom: none;
    }}

    /* Buttons styling */
    .stButton>button {{
        border-radius: 6px;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }}

    /* Defense badge for live demo indicator */
    .defense-active-pill {{
        display: inline-block;
        background-color: #1E3A2F;
        color: #48BB78;
        border: 1px solid #2F855A;
        font-size: 0.72rem;
        padding: 2px 7px;
        border-radius: 4px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
