import requests
import json

url = "http://localhost:11434/api/chat"

def llama3(email_body):
    # 🏷️ Formulate the complete prompt
    prompt = f"Classify the following email into one of the predefined categories: Adjustment, AU Transfer, Closing Notice, Commitment Change, Fee Payment, Money Movement - Inbound, Money Movement - Outbound.\n\nEmail Body:\n{email_body}"
    data = {
        "model": "llama3.2",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False,
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=data)

    # Print the entire response for debugging
    print("Raw Response:", response.json())

    # Handle response structure and errors
    try:
        # Extracting the nested "content" field from "message"
        return response.json()["message"]["content"]
    except KeyError:
        return "Error: Invalid response structure"