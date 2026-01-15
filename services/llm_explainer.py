from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def explain_demand_supply(analysis_result: dict) -> str:
    """
    LLM only EXPLAINS provided NVIDIA data.
    """

    prompt = f"""
You are a NVIDIA operations analyst AI.

You are given VERIFIED DATA below.
Do NOT add new facts.
Do NOT hallucinate.
Only explain and summarize.

DATA:
{analysis_result}

Explain:
- Demand situation
- Supply constraints
- Risk level
- Short recommendation
"""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=400
    )

    return completion.choices[0].message.content
