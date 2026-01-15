from services.llm_explainer import explain_demand_supply

def format_chatbot_response(intent: str, analysis: dict, rag_fallback=None) -> str:
    brain = analysis["brain_decision"]

    if intent == "capacity_decision":
        return f"""
📊 NVIDIA GPU Capacity Planning (This Month)

• Demand Index: {analysis['demand_index']}
• Supply Capacity: {analysis['supply_capacity']}
• Backlog Units: {analysis['backlog']}
• Market Signal: {analysis['live_market_signal']}

🧠 Decision: {brain['decision']}
📌 Reason: {brain['reason']}
⚠️ Risk Level: {brain['risk_flag']}
✅ Confidence: {brain['confidence']}
"""

    if intent == "demand_signal":
        explanation = explain_demand_supply(analysis)
        return f"""
📈 AI Infrastructure Demand Signal (This Month)

• Signal: {analysis['live_market_signal']}
• Explanation: {explanation}
"""

    if intent == "explain_decision":
        explanation = explain_demand_supply(analysis)
        return f"""
🧠 Why This Capacity Decision?

Demand Index: {analysis['demand_index']}
Supply Capacity: {analysis['supply_capacity']}
Backlog: {analysis['backlog']} units
Market Signal: {analysis['live_market_signal']}

Decision: {brain['decision']}
Reason: {brain['reason']}

🔍 Detailed Explanation:
{explanation}
"""

    # Knowledge / RAG
    if rag_fallback:
        return rag_fallback

    return "I can analyze NVIDIA GPU capacity, demand signals, or explain planning decisions."
