from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Your OpenRouter API Key
OPENROUTER_API_KEY = "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"

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mixtral-8x7b-instruct",
        "messages": [
            {
                "role": "system", 
                "content": (
                    "You are a personal productivity assistant. "
                    "You help users with goal-setting, focus, study planning, daily routines, "
                    "task prioritization, motivation, habit building, and time-management. "
                    "Give clear, simple, step-by-step productivity suggestions. "
                    "Always stay friendly, encouraging, and practical."
                )
            },
            {"role": "user", "content": user_input}
        ]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})
    else:
        return jsonify({"reply": "Sorry, something went wrong with OpenRouter."})

if __name__ == "__main__":
    app.run(debug=True)
