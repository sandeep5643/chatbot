from flask import Flask, render_template, request, jsonify
from services.openai_service import generate_response
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"reply": "Invalid request"}), 400

    user_msg = data["message"]

    # 🔥 PURE BRAIN CALL
    reply = generate_response(user_msg)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)