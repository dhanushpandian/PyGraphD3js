import openai
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

def ai(user_input):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    messages = [
        {
            "role": "system",
            "content": "You are an AI specialized in medical analysis,so answer the query and add some hidden insights only relevent to the query asked  . Provide structured answers in plain text, no extra formatting."
        },
        {
            "role": "user",
            "content": f"Generate an plain text response using only insights from the data: {user_input}"
        }
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0
        )

        raw_response = response.choices[0].message.content.strip()
        print("AI Raw Response:", raw_response)

        return {"response": raw_response}  # Return as JSON for Flask

    except Exception as e:
        return {"error": f"OpenAI API Error: {str(e)}"}



    # GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # if not GEMINI_API_KEY:
    #     return {"error": "GEMINI_API_KEY not found in environment variables."}

    # url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

    # payload = {
    #     "contents": [{"parts": [{"text": f"Convert this text into JSON: {messages}"}]}]
    # }
    # headers = {"Content-Type": "application/json"}

    # try:
    #     response = requests.post(url, headers=headers, json=payload)
    #     response_data = response.json()

    #     # Print full API response for debugging
    #     print("Gemini API Response:", response_data)

    #     # Extract text response properly
    #     if "candidates" in response_data:
    #         return json.loads(response_data["candidates"][0]["content"]["parts"][0]["text"])

    #     return {"error": "Gemini API failed", "response": response_data}

    # except Exception as e:
    #     return {"error": f"Gemini API Error: {str(e)}"}


if __name__ == "__main__":
    messages = """Received message for Groq: give me consice answers only from the graph data answering the question what types of protiens are there in the graph about autism?
'"""
    print("output now:",ai(messages))