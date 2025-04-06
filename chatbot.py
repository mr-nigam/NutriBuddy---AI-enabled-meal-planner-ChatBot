import google.generativeai as genai
genai.configure(api_key = "AIzaSyB7SIduhYVQoSSoyJp3v87zeeYQ4bsQMi0")
model = genai.GenerativeModel("gemini-2.0-flash")

user_memory = {
    "diet": None,
    "allergies": [],
    "goals": None,
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

def  nutrition_chatbot(message):
    update_memory(message)


    memory_summary = f"""
User Preferences:
- Diet: {user_memory['diet'] or 'not set'}
- Allergies: {', '.join(user_memory['allergies']) or 'none'}
- Goals: {user_memory['goals'] or 'not specified'}
"""


    prompt = f"""
You are a certified nutrition expert chatbot.

You MUST answer ONLY food, nutrition, and diet-related questions.
Be brief and specific.
Format in 1–3 bullet points or short sentences.
If the question is off-topic, politely decline.

Personalize responses based on this memory:
{memory_summary}

Now respond to the user query: "{message}"
"""

    response = model.generate_content(prompt,generation_config={"temperature": 0.7, "top_p": 1.0,"top_k": 1})
    return response.text.strip()

print("Welcome to the Nutrition Chatbot.")
print("Type 'exit' to end the chat.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Stay healthy! Goodbye.")
        break

    reply = nutrition_chatbot(user_input)
    print("Bot:", reply)

