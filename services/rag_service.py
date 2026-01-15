# from services.vector_db import build_vector_db
# from services.document_loader import load_documents
# from services.llm_client import llm

# # Load once at startup (GOOD PRACTICE)
# docs = load_documents()
# vector_db = build_vector_db(docs)

# CONFIDENCE_THRESHOLD = 0.65   # 🔥 Industry standard

# def rag_answer(query: str) -> str:
#     # 🔹 similarity + score (IMPORTANT)
#     results = vector_db.similarity_search_with_score(query, k=4)

#     if not results:
#         return "This information is not available in the provided NVIDIA documents."

#     # 🔹 Best similarity score
#     best_score = max([score for _, score in results])

#     # 🔹 Confidence gate (NO HALLUCINATION)
#     if best_score < CONFIDENCE_THRESHOLD:
#         return "This information is not available in the provided NVIDIA documents."

#     # 🔹 Build clean context (NO metadata)
#     context = "\n\n---\n\n".join([
#         doc.page_content for doc, _ in results
#     ])

#     prompt = f"""
# You are an enterprise-grade NVIDIA analyst AI.

# STRICT RULES:
# - Answer ONLY using the provided context.
# - Do NOT mention PDF names, page numbers, document titles, or sources.
# - Do NOT say "according to the document" or "context says".
# - Do NOT add assumptions or external knowledge.
# - If the context does not clearly support the answer, say:
#   "This information is not available in the provided NVIDIA documents."

# Answer Structure:
# 1. Direct Answer: Yes/No + one-sentence summary
# 2. Key Reasons for Demand Growth
# 3. Sources of Demand
# 4. Scale & Trends
# 5. Supply Fulfillment Outlook (only if mentioned)
# 6. Summary for Decision Making

# Keep it professional, factual, and concise.

# Context:
# {context}

# Question:
# {query}
# """

#     return llm(prompt).strip()



from services.vector_db import build_vector_db
from services.document_loader import load_documents
from services.llm_client import llm
from services.live_market_service import fetch_nvda_live_data

# Load once at startup
docs = load_documents()
vector_db = build_vector_db(docs)

CONFIDENCE_THRESHOLD = 0.65


def rag_answer(query: str) -> str:
    results = vector_db.similarity_search_with_score(query, k=4)

    if not results:
        return "This information is not available in the provided NVIDIA documents."

    best_score = max(score for _, score in results)

    if best_score < CONFIDENCE_THRESHOLD:
        return "This information is not available in the provided NVIDIA documents."

    context = "\n\n---\n\n".join(
        doc.page_content for doc, _ in results
    )

    live_data = fetch_nvda_live_data()

    prompt = f"""
You are an enterprise-grade NVIDIA market intelligence AI.

STRICT RULES:
- Use ONLY the information provided below.
- Do NOT mention PDFs, documents, sources, or page numbers.
- Do NOT guess missing data.
- If information is missing, clearly say so.

Answer Format:
1. Direct Answer
2. Key Drivers
3. Demand Sources
4. Market Trend (Historical vs Current)
5. Supply Outlook (if mentioned)
6. Decision Summary

Historical Context:
{context}

Live Market Signal:
{live_data}

Question:
{query}
"""

    return llm(prompt).strip()
