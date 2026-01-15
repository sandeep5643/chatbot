# # services/capacity_brain_explainer.py

# from groq import Groq
# import os
# from dotenv import load_dotenv

# load_dotenv()
# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# def explain_capacity_decision(user_question: str, analysis: dict) -> str:
#     """
#     Explains capacity decision strictly from brain output + analysis.
#     NO new facts.
#     """

#     prompt = f"""
#     You are an NVIDIA capacity planning analyst AI.

#     STRICT RULES:
#     - brain_decision is FINAL
#     - Do NOT contradict decision
#     - Do NOT re-evaluate risk
#     - Explain decision clearly using given data only

#     USER QUESTION:
#     {user_question}

#     DATA:
#     {analysis}

#     Explain:
#     - Why this decision was taken
#     - Whether expansion is recommended or not
#     - What signals should change the decision in future
#     """


#     completion = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.2,
#         max_tokens=450
#     )

#     return completion.choices[0].message.content


# services/capacity_brain_explainer.py

from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def explain_capacity_decision(user_question: str, analysis: dict) -> str:
    brain = analysis["brain_decision"]

    prompt = f"""
You are an NVIDIA capacity planning explanation AI.

IMPORTANT:
- The FINAL decision is already made.
- You MUST NOT change or contradict it.
- You MUST NOT re-evaluate risk or demand.
- You ONLY explain the decision.

FINAL DECISION (LOCKED):
Decision: {brain['decision']}
Risk Level: {brain['risk_flag']}
Confidence: {brain['confidence']}

SUPPORTING SIGNALS:
Demand Index: {analysis['demand_index']}
Supply Capacity: {analysis['supply_capacity']}
Backlog Units: {analysis['backlog']}
Market Signal: {analysis['live_market_signal']}

USER QUESTION:
{user_question}

Explain in clear business language:
1. Why this decision was taken
2. Whether capacity expansion is recommended now
3. What specific signal changes could alter this decision in the future

Do NOT introduce new metrics.
Do NOT contradict the locked decision.
"""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=350
    )

    return completion.choices[0].message.content.strip()

