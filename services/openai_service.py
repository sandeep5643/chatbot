import os
import re
from dotenv import load_dotenv
from groq import Groq

from services.demand_classifier import classify_user_demand
from services.analysis_engine import analyze_demand_vs_supply
from services.llm_explainer import explain_demand_supply
from services.rag_service import rag_answer
from services.live_market_service import fetch_nvda_live_data, fetch_nvda_historical_price
from services.brain_capacity_planner import capacity_planning_brain
from services.capacity_brain_explainer import explain_capacity_decision



load_dotenv()

# =========================
# Initialize Groq Client
# =========================
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# =========================
# NVIDIA Specific System Prompt
# =========================
NVIDIA_SYSTEM_PROMPT = """
You are an AI assistant specialized ONLY in NVIDIA.

Your role:
- Answer questions related to NVIDIA products, technologies, services, and research
- Examples: GPUs, CUDA, TensorRT, NVIDIA AI, DGX, Jetson, Omniverse, NVIDIA drivers

Strict rules:
- If a question is NOT related to NVIDIA, respond with exactly:
  "I can only help with NVIDIA-related questions."

Answer style:
- Clear, structured, professional
- Be factual and accurate
- Do NOT hallucinate
"""

# =========================
# Utility: Clean model tokens
# =========================
def clean_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"<\/?s>|<\/?\/s>|\[\/s\]|~~", "", text)
    return text.strip()

# =========================
# Main Entry Function
# =========================
def generate_response(user_msg: str) -> str:
    try:
        intent = classify_user_demand(user_msg)

        # =========================
        # LIVE MARKET
        # =========================
        if intent == "LIVE_MARKET_DATA":
            return fetch_live_market_answer(user_msg)

        # =========================
        # CAPACITY PLANNING (🔥 NEW)
        # =========================
        if intent == "CAPACITY_PLANNING":
            analysis = analyze_demand_vs_supply(region="global")

            # Combine brain + analysis
            combined_analysis = {
                **analysis,
                "brain_decision": analysis["brain_decision"]
            }

            explanation = explain_capacity_decision(
                user_msg,
                combined_analysis
            )

            return f"""
        🧠 NVIDIA GPU Capacity Planning Analysis

        Decision: {analysis['brain_decision']['decision']}
        Risk Level: {analysis['brain_decision']['risk_flag']}
        Confidence: {analysis['brain_decision']['confidence']}

        📊 Key Signals:
        • Demand Index: {analysis['demand_index']}
        • Supply Capacity: {analysis['supply_capacity']}
        • Backlog Units: {analysis['backlog']}
        • Market Signal: {analysis['live_market_signal']}

        🔍 Explanation:
        {explanation}
        """

        # =========================
        # DEMAND / SUPPLY
        # =========================
        if intent in ["DEMAND_SIGNAL", "SUPPLY_STATUS"]:
            return rag_answer(user_msg)

        if intent == "DEMAND_SUPPLY_ANALYSIS":
            analysis = analyze_demand_vs_supply(region="global")
            return explain_demand_supply(analysis)

        # =========================
        # DEFAULT NVIDIA Q&A
        # =========================
        return generate_nvidia_llm_answer(user_msg)

    except Exception as e:
        print("❌ openai_service error:", e)
        return get_fallback_response(user_msg)


# =========================
# NVIDIA LLM Answer
# =========================
def generate_nvidia_llm_answer(user_msg: str) -> str:
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": NVIDIA_SYSTEM_PROMPT},
            {"role": "user", "content": user_msg}
        ],
        temperature=0.3,
        max_tokens=800
    )

    return clean_text(completion.choices[0].message.content)

# def fetch_live_market_answer(user_msg):
#     data = fetch_nvda_live_data()
#     if not data:
#         return "Sorry, live market data is not available at the moment."

#     # ✅ Use correct keys
#     return (
#         f"NVIDIA (NVDA) live price: ${data['current_price']:,} "
#         f"(day high {data['high']:,}, day low {data['low']:,})."
#     )

def fetch_live_market_answer(user_msg):
    """
    Detect if user asked about current vs previous year price
    """
    user_lower = user_msg.lower()

    # If user asks about previous year, fetch historical
    if "previous year" in user_lower or "historical" in user_lower:
        hist_price = fetch_nvda_historical_price("2025-12-31")
        if hist_price:
            return f"NVIDIA (NVDA) closing price on 2025-12-31: ${hist_price}"
        else:
            return "Sorry, historical data for NVIDIA is not available."

    # Default → live market price
    data = fetch_nvda_live_data()
    if not data:
        return "Sorry, live market data is not available at the moment."

    return (
        f"NVIDIA (NVDA) live price: ${data['current_price']:,} "
        f"(day high {data['high']:,}, day low {data['low']:,})."
    )


# =========================
# Fallback Responses (NO HALLUCINATION)
# =========================
def get_fallback_response(user_msg: str) -> str:
    user_lower = user_msg.lower()

    nvidia_keywords = [
        "nvidia", "cuda", "gpu", "rtx", "gtx",
        "tensor", "dgx", "jetson", "omniverse",
        "driver", "dlss", "ai"
    ]

    if any(keyword in user_lower for keyword in nvidia_keywords):
        return (
            "⚠️ I'm temporarily unable to retrieve NVIDIA data.\n\n"
            "Please try again shortly."
        )

    return "I can only help with NVIDIA-related questions."

# =========================
# Local Testing
# =========================
if __name__ == "__main__":
    print("✅ openai_service loaded")

    q1 = "How fast is Generative AI driving demand for NVIDIA GPUs?"
    print("Q:", q1)
    print("A:", generate_response(q1))

    q2 = "What is React JS?"
    print("\nQ:", q2)
    print("A:", generate_response(q2))
