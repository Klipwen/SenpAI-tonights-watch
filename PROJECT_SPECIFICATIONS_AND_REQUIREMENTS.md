# SenpAI: Tonight's Watch — Project Architecture & Specification Blueprint

**Course:** Applied AI / Applications of Data Science and Artificial Intelligence (Final Assessment Week 18)  
**Group Members:** Judd Kristoffer Mayuela, Gee Caliph A. Juen, Bryne Kendrick P. Nuñez  
**Project:** SenpAI: Tonight's Watch (Streamlit AI Chatbot)

---

## 1. Team Decisions & Confirmed Technical Choices

The following decisions have been locked in by the team:

* **LLM Engine:** Google Gemini (`gemini-1.5-flash` / `gemini-2.0-flash`) via `google-genai` / `google-generativeai`.
  * *Reason:* Generous free tier, fast response times, natively supports function/tool calling, and deploys cleanly to Streamlit Community Cloud.
* **Rubric Bonus ("Going Further"):** **Agentic Tool Calling via Jikan API (MyAnimeList)**.
  * *Why this is the best choice:* Directly satisfies the rubric's "Agentic features" requirement (function calling). Pulls live anime runtimes, exact episode counts, synopsis, and official poster art. We will also include Streamlit caching (`@st.cache_data`) so results are instant and immune to campus Wi-Fi hiccups during your live demo.
* **Prompt Hacking Defenses (Approved):**
  1. **Pre-flight Guardrail Filter:** Intercepts jailbreaks, prompt extraction, and roleplay exploits before reaching the API.
  2. **XML Input Encapsulation:** Encloses user input within `<user_query>` tags.
  3. **Sandwich Defense / Post-prompting:** Re-attaches safety and scope constraints after user input.
* **Part 4 (UI / UX Decisions):**
  * **STRICT UI REQUIREMENT — ZERO EMOJIS (HUMAN-CRAFTED DESIGN):**
    * Absolutely **no emojis** anywhere in the UI, button labels, badge ranks, or bot responses.
    * No generic AI-style emoji clutter (`🤖`, `🥇`, `🥈`, `🥉`, `🗑️`, `⭐`, `⚖️`, `✨`).
    * Use clean, modern typographic elements, sleek SVG line icons, or minimalist CSS badge pills (e.g. geometric `[ 1 ]`, `[ 2 ]`, `[ 3 ]` tags).
    * Buttons must use professional, clean text labels: `"Add to Watchlist"`, `"Clear Watchlist"`, `"Compare"`, `"Find Similar"`.
    * System Prompt updated: SenpAI must strictly never output emojis, maintaining a natural, human conversational tone.
  * *[Pending team discussion / input on poster cards & classical preset]*

---

## 2. Technical Architecture & File Organization

Once approved, here is the clean file layout that will be set up in your repository:

```
C:\Users\Gee Caliph\Desktop\Programming\System\
│
├── app.py                     # Main Streamlit application entry point
├── config.py                  # App configuration, constants, and environment variables
├── requirements.txt           # Python dependencies (streamlit, google-genai / openai, requests, etc.)
│
├── core/
│   ├── __init__.py
│   ├── llm_client.py          # Unified wrapper for LLM calls (Gemini/Groq/OpenAI)
│   ├── prompt_manager.py      # System prompt, XML packaging, and sandwich defenses
│   ├── guardrails.py          # Input sanitizer & prompt-injection detection functions
│   └── tools.py               # Anime lookup tool (Jikan API integration for real data & posters)
│
├── ui/
│   ├── __init__.py
│   ├── components.py          # Sidebar quiz form, watchlist widget, chat cards
│   └── styles.py              # Custom CSS for polished, student-friendly theme
│
├── .streamlit/
│   ├── config.toml            # Streamlit theme settings (fonts, colors, layout)
│   └── secrets.toml.example   # Template for API keys (never commit secrets.toml)
│
├── README.md                  # Comprehensive documentation, setup guide, and rubric checklist
└── presentation/
    └── slides_outline.md      # Ready-to-use outline for your 5-minute presentation & live demo
```

---

## 3. Rubric Compliance Matrix

| Requirement | Course Rubric Standard | How SenpAI Will Satisfy It |
|---|---|---|
| **LLM Chatbot** | API-driven LLM conversation | Gemini / Groq / OpenAI with conversation history stored in `st.session_state.messages` |
| **Engineered Prompt** | Role, persona, shot-based / few-shot, constraints | Strict SenpAI senpai persona, 3-pick format, time-budget constraints, classical music ties |
| **Prompt Defenses** | At least 2 active defenses | 1. Input sanitization filter<br>2. XML input encapsulation<br>3. Post-prompt sandwich reinforcement |
| **Deployed & Accessible** | Streamlit Cloud + Public GitHub | Streamlit Community Cloud deployment with `secrets.toml` key management |
| **Recommended / Bonus** | RAG / Agentic / Tools / Data Integration | Jikan API integration for live anime metadata, exact runtimes, and official cover art |
| **Live Attack Demo** | Show defenses blocking an attack | Prepared test attacks (e.g., jailbreak attempt, prompt leak attempt) with graceful refusal |

---

## 4. Next Steps

1. Review this specification with your teammates (**Judd, Gee Caliph, Bryne**).
2. Confirm your preferred:
   - **LLM choice** (Gemini recommended)
   - **API key readiness**
   - Any extra UI tweaks or features you'd like added.
3. Once you give the green light, we will generate the complete, modular code ready for local testing, GitHub upload, and Streamlit Community Cloud deployment!
