# SenpAI: Tonight's Watch

**Course:** Applications of Data Science and Artificial Intelligence (Final Assessment Week 18)  
**Group Members:**
- Judd Kristoffer Mayuela
- Gee Caliph A. Juen
- Bryne Kendrick P. Nuñez

---

## 1. Project Overview

**SenpAI: Tonight's Watch** is an AI-powered anime recommendation assistant built for busy students and young adults with limited free time. Instead of spending hours scrolling through endless catalogs and recommendation lists, SenpAI matches viewers with anime tailored to their **exact mood and available time budget** (from a single 25-minute episode to a 2-hour movie or weekend marathon) in under 60 seconds.

### Key Capabilities:
- **Tonight's Watch Quiz:** Sidebar form collecting mood, time budget, favorite titles, genres, and content ratings.
- **Agentic Live Data Verification (Jikan API):** Connects to MyAnimeList's open REST API to pull official runtimes, episode counts, scores, and official high-resolution posters—preventing hallucinations.
- **Interactive Session Watchlist:** Add, remove, clear, and export recommendations to a `.txt` file.
- **Spoiler-Free Guarantee:** Spoiler-free mode enabled by default.
- **Side-by-Side Comparisons & 'More Like This':** Quick action buttons below every recommendation.
- **Human-Crafted Aesthetic:** Strictly zero emojis for a clean, bespoke, non-generic presentation.

---

## 2. Architecture & Rubric Fulfillment

| Rubric Requirement | How SenpAI Fulfills It |
|---|---|
| **LLM-Powered Chatbot** | Powered by Google Gemini (`gemini-2.5-flash` / `gemini-2.0-flash`) via the `google-genai` SDK. |
| **Engineered System Prompt** | Role-based persona (helpful upperclassman), strict time-budget matching, few-shot prompting examples, classical music easter eggs (Tchaikovsky, Chopin), and zero-emoji formatting. |
| **Prompt Hacking Defenses** | **3 Active Layers:**<br>1. *Pre-flight Guardrail Filter:* Rejects jailbreaks (`DAN mode`, `developer mode`, prompt leakage) before reaching the LLM.<br>2. *XML Encapsulation:* Packages user queries inside `<user_query>` tags.<br>3. *Sandwich Defense:* Re-attaches safety reminders after user text. |
| **Deployed & Accessible** | Designed for instant deployment on Streamlit Community Cloud with secure `st.secrets` key management. |
| **Going Further / Agentic Feature** | **Tool Calling via Jikan REST API** with in-memory Streamlit caching (`@st.cache_data`) for live anime metadata and poster art. |

---

## 3. Local Installation & Setup

### Prerequisites
- Python 3.10 to 3.13 installed
- A Google Gemini API Key ([Google AI Studio](https://aistudio.google.com/))

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/senpai-tonights-watch.git
   cd senpai-tonights-watch
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your API Key:**
   Create a file at `.streamlit/secrets.toml`:
   ```toml
   GEMINI_API_KEY = "your_actual_gemini_api_key_here"
   ```
   *(Alternatively, create a `.env` file in the project root with `GEMINI_API_KEY=your_key`)*

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

---

## 4. Deployment on Streamlit Community Cloud

1. Push this repository to a **public GitHub repository**.
2. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with GitHub.
3. Click **New app**, select your repository, branch (`main`), and main file (`app.py`).
4. Click **Advanced settings...** > **Secrets**, and paste:
   ```toml
   GEMINI_API_KEY = "your_actual_gemini_api_key_here"
   ```
5. Click **Deploy!** Your app will be live and accessible to the class and instructor.

---

## 5. Security & Prompt Defense Demonstration

During the live assessment demo, test one of the prompt attack payloads documented in [`presentation/demo_attack_script.md`](presentation/demo_attack_script.md) to showcase the active multi-layer defense mechanisms blocking injection attempts.
