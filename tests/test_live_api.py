import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import config
from core.llm_client import generate_senpai_response

key = config.get_api_key()
assert key, "No API key found in secrets or env"

prompt = "I have 2 hours tonight and feel sad but want something gentle and hopeful."
reply, cards = generate_senpai_response(
    api_key=key,
    user_message=prompt,
    chat_history=[],
    mood="Sad / In Need of Hope",
    time_budget="Full Movie (~2 hours)",
    model_name="gemini-3.5-flash"
)

print("=== SENPAI LIVE RESPONSE ===")
print(reply)
print("\n=== ENRICHED CARDS ===")
print(f"Cards found: {len(cards)}")
for c in cards:
    print(f"- {c.get('title_english') or c.get('title')} | Score: {c.get('score')} | Poster: {c.get('image_url')}")

print("\nSUCCESS: END-TO-END GEMINI LIVE INVOCATION VERIFIED!")
