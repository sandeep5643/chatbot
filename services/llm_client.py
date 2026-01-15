import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def llm(prompt: str) -> str:
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Answer strictly from provided context."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=700
    )
    return completion.choices[0].message.content
