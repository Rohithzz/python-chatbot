from openai import OpenAI
import google.generativeai as genai
import os

# OpenAI setup
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Gemini setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-1.5-flash")  # free tier model

def chat_with_ai(prompt):
    try:
        # Try OpenAI first
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("⚠️ OpenAI failed, falling back to Gemini:", str(e))
        # Fallback to Gemini
        try:
            response = gemini_model.generate_content(prompt)
            return response.text.strip()
        except Exception as ge:
            return f"Both OpenAI and Gemini failed: {ge}"

if __name__ == "__main__":
    print("Chatbot ready! Type 'quit' to exit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Chatbot: Goodbye! 👋")
            break
        response = chat_with_ai(user_input)
        print("Chatbot:", response)
