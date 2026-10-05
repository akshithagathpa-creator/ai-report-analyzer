from flask import Flask, render_template,request
from google import genai
import os
import json

app = Flask(__name__)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask_ai():
    try:
        data = request.get_json()
        user_message = data["message"]

        prompt = f"""
Analyze this user message:

{user_message}

Return ONLY valid JSON in exactly this format:

{{
    "category": "short category",
    "urgency": "Low, Medium, or High",
    "action": "short recommended action"
}}
"""

        response = client.interactions.create(
            model="gemini-3.8-flash",
            input=prompt
        )

        result = json.loads(response.output_text)

        return result

    except Exception as e:
        print("Error:", e)

        return {
            "error": "Something went wrong while analyzing the issue."
        }, 500
if __name__ == "__main__":
    app.run(debug=True)