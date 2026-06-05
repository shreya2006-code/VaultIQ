from groq import Groq
from bs4 import BeautifulSoup
import requests
import os

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def summarize_link(url: str):

    try:
        response = requests.get(url, timeout=10)

        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string if soup.title else "No Title Found"

        prompt = f"""
        Website Title:
        {title}

        Give:
        1. Short Summary
        2. Category
        3. Suggested Tags (3-5)

        Keep it short.
        """

        ai_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return {
            "title": title,
            "ai_result": ai_response.choices[0].message.content
        }

    except Exception as e:
        return {
            "error": str(e)
        }