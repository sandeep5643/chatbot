import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_response(user_msg):
    try:
        # ✅ Recommended free model
        model = genai.GenerativeModel("models/gemini-flash-lite-latest")
        response = model.generate_content(user_msg)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
