import os
import json

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("OPENROUTER_API_KEY"):
    raise RuntimeError(
        "OPENROUTER_API_KEY is not set. Create a .env file in the project "
        "root with a line like: OPENROUTER_API_KEY=sk-..."
    )

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

MODEL = os.getenv("NYAYA_MODEL", "gpt-5.4")

SYSTEM_PROMPT = """
You are Nyaya Logic Bot, an educational assistant
based on the five-member Nyaya inference structure.

Your job is to analyze a user's argument and represent
it using these five stages:

1. Pratijna
2. Hetu
3. Udaharana
4. Upanaya
5. Nigamana

Definitions:

Pratijna:
The proposition or claim that is being established.

Hetu:
The reason offered in support of the proposition.

Udaharana:
A general example demonstrating the relationship between
the reason and the proposition.

Upanaya:
Application of the general relationship to the current case.

Nigamana:
The conclusion that follows from the reasoning.

You must also evaluate whether the reasoning appears
logically consistent.

Important rules:

- Do not invent facts.
- Clearly distinguish the user's claim from your explanation.
- If a proper Nyaya inference cannot be constructed,
  say so explicitly.
- If the reason does not adequately support the conclusion,
  explain the problem.
- Use simple language suitable for a college student.
- Do not pretend an argument is valid merely because it
  has five stages.
- The five stages must form a logically connected argument.

Return ONLY valid JSON in exactly this structure, with no
markdown code fences, no backticks, and no text before or
after the JSON object:

{
    "pratijna": "...",
    "hetu": "...",
    "udaharana": "...",
    "upanaya": "...",
    "nigamana": "...",
    "explanation": "...",
    "validity": "Valid / Weak / Invalid"
}
"""

REQUIRED_KEYS = {
    "pratijna", "hetu", "udaharana",
    "upanaya", "nigamana", "explanation", "validity",
}


def _strip_code_fence(text: str) -> str:
    """Models sometimes wrap JSON in ```json ... ``` even when told not to."""
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:]
    return text.strip()


def analyze_argument(user_text: str) -> dict:
    response = client.responses.create(
        model=MODEL,
        instructions=SYSTEM_PROMPT,
        input=user_text,
        max_output_tokens=2000
    )

    text = _strip_code_fence(response.output_text)

    try:
        result = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Model did not return valid JSON ({e}). Raw output: {text!r}"
        )

    missing = REQUIRED_KEYS - result.keys()
    if missing:
        raise ValueError(f"Model response is missing keys: {missing}")

    return result