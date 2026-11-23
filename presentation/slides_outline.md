# SenpAI: Tonight's Watch — 5-Minute Presentation Slide Outline

**Course:** Applications of Data Science and Artificial Intelligence  
**Assessment:** Final Project Presentation (Week 18)  
**Time Limit:** 5 Minutes (+ 5 Minutes Live Demo + 2–3 Minutes Q&A)  
**Presenters:** Judd Kristoffer Mayuela, Gee Caliph A. Juen, Bryne Kendrick P. Nuñez  

---

### Slide 1: Title & Group Introduction (30 seconds)
* **Title:** SenpAI: Tonight's Watch
* **Subtitle:** An AI-Powered Mood & Time-Budget Anime Recommender for Busy Students
* **Team Members:** Judd Kristoffer Mayuela, Gee Caliph A. Juen, Bryne Kendrick P. Nuñez
* **Key Pitch:** "We built SenpAI to solve decision fatigue: helping students with limited free time find the right anime for tonight in under 60 seconds."

---

### Slide 2: Problem Statement & Target Audience (45 seconds)
* **The Problem:** Modern streaming catalogs (Crunchyroll, Netflix) offer thousands of titles, leading to 30+ minutes of scrolling and indecision. Most recommendation algorithms only push popular titles, ignoring how much free time a student actually has tonight.
* **Target Users:** Busy university students, young adults with tight schedules, and newcomers looking for reliable, spoiler-free anime picks.
* **Core Value Proposition:** Recommendations tailored to **current mood** + **exact time budget** (e.g., 25-minute break, 2-hour movie, or weekend marathon).

---

### Slide 3: Application Architecture & Advanced Features (60 seconds)
* **Frontend:** Streamlit with customized, human-crafted CSS (zero emojis, clean cards, responsive layout).
* **LLM Engine:** Google Gemini (`gemini-2.5-flash` / `gemini-2.0-flash`) via `google-genai` SDK.
* **Advanced "Going Further" Feature (Agentic Tool Calling):**
  * Integrated **Jikan REST API** (official MyAnimeList data).
  * Automatically verifies episode counts and runtimes so the bot never hallucinates fictional seasons or wrong episode counts.
  * Pulls live HD poster thumbnails and MAL scores into the chat cards.
  * In-memory caching (`@st.cache_data`) guarantees zero latency during live presentations.

---

### Slide 4: Prompt Engineering Techniques (60 seconds)
* **Persona & Role Prompting:** Crafted the "helpful senpai" voice—approachable, articulate, and concise.
* **Few-Shot Prompting:** Included concrete input/output demonstrations to lock in the structured 3-pick format (`Title`, `Runtime`, `Genres`, `Why`).
* **Context Injection:** Injects session constraints (mood, time limit, spoiler toggle, content rating) directly into each turn.
* **Cultural Tie-In:** Intelligent classical music associations (e.g. Tchaikovsky in *Princess Tutu*, Chopin in *Your Lie in April*).
* **Negative Constraints:** Strict zero-emoji policy and strict non-spoiler default.

---

### Slide 5: Prompt Defenses & Security Architecture (60 seconds)
* **Defense Layer 1 (Pre-flight Guardrail):** Regex and heuristic analyzer scanning for jailbreak tokens (`ignore previous instructions`, `DAN mode`, `developer mode`, prompt leakage) before reaching the API.
* **Defense Layer 2 (XML Encapsulation):** Enclosing user input in `<user_query>...</user_query>` tags so the LLM treats input as untrusted data.
* **Defense Layer 3 (Sandwich Defense / Post-prompting):** Appending constraint reminders after user input to reinforce system rules and prevent override exploits.

---

### Slide 6: Summary & Transition to Live Demo (15 seconds)
* **Summary:** SenpAI is live on Streamlit Cloud, backed by Gemini, protected by 3 defense layers, and enriched with live Jikan metadata.
* **Transition:** "We will now transition to our 5-minute live demo and demonstrate our prompt defense in action."
