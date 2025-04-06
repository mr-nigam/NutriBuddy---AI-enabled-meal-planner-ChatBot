from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS
import os
app = Flask(__name__)
CORS(app)

# Gemini API setup
genai.configure(api_key="AIzaSyB7SIduhYVQoSSoyJp3v87zeeYQ4bsQMi0")
model = genai.GenerativeModel("gemini-2.0-flash")

# User memory
user_memory = {
    "diet": None,
    "allergies": [],
    "goals": [],
}

diet_keywords = ["vegan", "vegetarian", "keto", "paleo", "mediterranean"]
allergy_keywords = ["gluten", "peanuts", "soy", "dairy", "shellfish", "eggs"]
goal_keywords = ["weight loss", "muscle gain", "maintenance", "energy", "detox"]

def update_memory(message):
    msg = message.lower()
    for diet in diet_keywords:
        if diet in msg:
            user_memory["diet"] = diet
            break

    for allergy in allergy_keywords:
        if allergy in msg and allergy not in user_memory["allergies"]:
            user_memory["allergies"].append(allergy)

    for goal in goal_keywords:
        if goal in msg and goal not in user_memory["goals"]:
            user_memory["goals"].append(goal)

def nutrition_chatbot(message):
    update_memory(message)

    memory_summary = f"""
    User Preferences:
    - Diet: {user_memory['diet'] or 'not set'}
    - Allergies: {', '.join(user_memory['allergies']) or 'none'}
    - Goals: {', '.join(user_memory['goals']) or 'not specified'}
    """

    prompt = f"""
    You are a certified nutrition expert chatbot.

    You MUST answer ONLY food, nutrition, and diet-related questions.
    Be brief and specific.
    Format in 1-3 bullet points or short sentences.
    If the question is off-topic, politely decline.

    Personalize responses based on this memory:
    {memory_summary}

    Now respond to the user query: "{message}"
    """

    response = model.generate_content(prompt, generation_config={"temperature": 0.7, "top_p": 1.0, "top_k": 1})
    return response.text.strip()

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message")
    if not message:
        return jsonify({"response": "Please send a valid message."}), 400

    reply = nutrition_chatbot(message)
    return jsonify({"response": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port = port)
