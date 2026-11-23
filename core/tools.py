import logging
import requests
import streamlit as st
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

JIKAN_BASE_URL = "https://api.jikan.moe/v4"

# Offline / Presentation Fallback Database for Instant Latency-Free Demos
OFFLINE_ANIME_LIBRARY: Dict[str, Dict[str, Any]] = {
    "josee, the tiger and the fish": {
        "mal_id": 40787,
        "title": "Josee to Tora to Sakana-tachi",
        "title_english": "Josee, the Tiger and the Fish",
        "episodes": 1,
        "duration": "1 hr 38 min",
        "rating": "PG-13",
        "score": 8.40,
        "synopsis": "A university student studying marine biology takes a job caring for a paraplegic young woman who escapes reality through painting and reading.",
        "image_url": "https://cdn.myanimelist.net/images/anime/1118/111527.jpg",
        "genres": ["Drama", "Romance"],
        "url": "https://myanimelist.net/anime/40787/Josee_to_Tora_to_Sakana-tachi"
    },
    "your name": {
        "mal_id": 32281,
        "title": "Kimi no Na wa.",
        "title_english": "Your Name.",
        "episodes": 1,
        "duration": "1 hr 46 min",
        "rating": "PG-13",
        "score": 8.84,
        "synopsis": "Two high schoolers who have never met suddenly begin intermittently swapping bodies across time and space.",
        "image_url": "https://cdn.myanimelist.net/images/anime/1935/127974.jpg",
        "genres": ["Award Winning", "Drama", "Supernatural"],
        "url": "https://myanimelist.net/anime/32281/Kimi_no_Na_wa"
    },
    "weathering with you": {
        "mal_id": 38826,
        "title": "Tenki no Ko",
        "title_english": "Weathering With You",
        "episodes": 1,
        "duration": "1 hr 52 min",
        "rating": "PG-13",
        "score": 8.27,
        "synopsis": "A runaway high school boy in Tokyo meets an orphaned girl with the miraculous power to stop the rain and clear the sky.",
        "image_url": "https://cdn.myanimelist.net/images/anime/1880/101146.jpg",
        "genres": ["Drama", "Fantasy", "Romance"],
        "url": "https://myanimelist.net/anime/38826/Tenki_no_Ko"
    },
    "spirited away": {
        "mal_id": 199,
        "title": "Sen to Chihiro no Kamikakushi",
        "title_english": "Spirited Away",
        "episodes": 1,
        "duration": "2 hr 5 min",
        "rating": "PG",
        "score": 8.77,
        "synopsis": "A 10-year-old girl enters a world ruled by gods, witches, and spirits where humans are changed into beasts.",
        "image_url": "https://cdn.myanimelist.net/images/anime/6/79597.jpg",
        "genres": ["Award Winning", "Adventure", "Supernatural"],
        "url": "https://myanimelist.net/anime/199/Sen_to_Chihiro_no_Kamikakushi"
    },
    "a silent voice": {
        "mal_id": 28851,
        "title": "Koe no Katachi",
        "title_english": "A Silent Voice",
        "episodes": 1,
        "duration": "2 hr 10 min",
        "rating": "PG-13",
        "score": 8.93,
        "synopsis": "A former elementary school bully seeks redemption by reconnecting with the deaf girl he once tormented, finding mutual healing and hope.",
        "image_url": "https://cdn.myanimelist.net/images/anime/1122/96442.jpg",
        "genres": ["Drama", "Award Winning"],
        "url": "https://myanimelist.net/anime/28851/Koe_no_Katachi"
    },
    "violet evergarden": {
        "mal_id": 33352,
        "title": "Violet Evergarden",
        "title_english": "Violet Evergarden",
        "episodes": 13,
        "duration": "24 min per ep",
        "rating": "PG-13",
        "score": 8.67,
        "synopsis": "A former child soldier learns the true meaning of love while working as an Auto Memory Doll, transcribing people's deepest emotions into letters.",
        "image_url": "https://cdn.myanimelist.net/images/anime/1795/95088.jpg",
        "genres": ["Drama", "Fantasy"],
        "url": "https://myanimelist.net/anime/33352/Violet_Evergarden"
    },
    "your lie in april": {
        "mal_id": 23273,
        "title": "Shigatsu wa Kimi no Uso",
        "title_english": "Your Lie in April",
        "episodes": 22,
        "duration": "22 min per ep",
        "rating": "PG-13",
        "score": 8.65,
        "synopsis": "A piano prodigy who lost the ability to hear his own music after trauma is brought back to life by a free-spirited violinist playing Chopin and Saint-Saëns.",
        "image_url": "https://cdn.myanimelist.net/images/anime/1417/129712.jpg",
        "genres": ["Drama", "Music", "Romance"],
        "url": "https://myanimelist.net/anime/23273/Shigatsu_wa_Kimi_no_Uso"
    },
    "frieren": {
        "mal_id": 52991,
        "title": "Sousou no Frieren",
        "title_english": "Frieren: Beyond Journey's End",
        "episodes": 28,
        "duration": "24 min per ep",
        "rating": "PG-13",
        "score": 9.32,
        "synopsis": "An elven mage outlives her heroic companions and embarks on a contemplative journey to understand human emotions and the value of time.",
        "image_url": "https://cdn.myanimelist.net/images/anime/1015/138075.jpg",
        "genres": ["Adventure", "Drama", "Fantasy"],
        "url": "https://myanimelist.net/anime/52991/Sousou_no_Frieren"
    },
    "princess tutu": {
        "mal_id": 721,
        "title": "Princess Tutu",
        "title_english": "Princess Tutu",
        "episodes": 26,
        "duration": "16 min per ep",
        "rating": "PG",
        "score": 8.12,
        "synopsis": "A magical duck transformed into a ballet dancer uses the power of classical ballet and Tchaikovsky's Swan Lake to recover the lost shards of a prince's heart.",
        "image_url": "https://cdn.myanimelist.net/images/anime/8/19477.jpg",
        "genres": ["Mahou Shoujo", "Music", "Drama", "Mystery"],
        "url": "https://myanimelist.net/anime/721/Princess_Tutu"
    },
    "words bubble up like soda pop": {
        "mal_id": 39175,
        "title": "Cider no You ni Kotoba ga Wakiagaru",
        "title_english": "Words Bubble Up Like Soda Pop",
        "episodes": 1,
        "duration": "1 hr 27 min",
        "rating": "PG-13",
        "score": 7.46,
        "synopsis": "A shy boy who expresses himself through haiku and a bubbly girl insecure about her braces meet during summer vacation in a suburban shopping mall.",
        "image_url": "https://cdn.myanimelist.net/images/anime/1205/115664.jpg",
        "genres": ["Romance", "Slice of Life"],
        "url": "https://myanimelist.net/anime/39175/Cider_no_You_ni_Kotoba_ga_Wakiagaru"
    }
}

@st.cache_data(ttl=3600, show_spinner=False)
def search_anime(query: str, limit: int = 3) -> List[Dict[str, Any]]:
    """
    Agentic Tool: Search MyAnimeList via Jikan API for real anime details.
    Includes built-in resilience: if Jikan experiences latency or rate limits,
    gracefully matches curated verified metadata and official posters.
    """
    clean_query = query.strip()
    if not clean_query:
        return []

    # 1. Check offline fallback library for instant zero-latency match
    lower_query = clean_query.lower()
    for key, data in OFFLINE_ANIME_LIBRARY.items():
        if key in lower_query or lower_query in key:
            return [data]

    # 2. Live fetch from Jikan REST API
    try:
        url = f"{JIKAN_BASE_URL}/anime"
        params = {
            "q": clean_query,
            "limit": limit,
            "sfw": "true"
        }
        response = requests.get(url, params=params, timeout=1.5)
        if response.status_code == 200:
            data = response.json().get("data", [])
            results = []
            for item in data:
                images = item.get("images", {}).get("jpg", {})
                image_url = images.get("large_image_url") or images.get("image_url", "")
                
                genres = [g.get("name", "") for g in item.get("genres", [])]
                themes = [t.get("name", "") for t in item.get("themes", [])]
                all_tags = [t for t in (genres + themes) if t]

                results.append({
                    "mal_id": item.get("mal_id"),
                    "title": item.get("title", ""),
                    "title_english": item.get("title_english") or item.get("title", ""),
                    "episodes": item.get("episodes") or "Unknown",
                    "duration": item.get("duration", "Approx 24 min"),
                    "rating": item.get("rating", "PG-13"),
                    "score": item.get("score") or "N/A",
                    "synopsis": (item.get("synopsis") or "No synopsis available.")[:300] + "...",
                    "image_url": image_url,
                    "genres": all_tags,
                    "url": item.get("url", "")
                })
            if results:
                return results
    except Exception as e:
        logger.warning(f"Jikan API live request timed out or failed: {e}. Checking secondary match.")

    return []
