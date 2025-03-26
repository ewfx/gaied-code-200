import requests
import json
import re
import os

file_path = os.path.abspath("./model/topics_to_classify.json")  # Get absolute path
print("Looking for:", file_path)  # Debug print

with open(file_path, "r") as rules_file:
    rules = json.load(rules_file)


url = "http://localhost:11434/api/chat"

def llama3(email_body, attachment_content):
    # 🏷️ Formulate the complete prompt
    prompt = (
        "You are an expert in commercial lending services. Your task is to classify the given content into one or more request types and Sub Request Types provided in the topics_to_classify.json file. "
        "The classification must maintain the hierarchy between request types and their associated sub-request types as specified in the topics_to_classify.json. "
        "Sub-request types should never be classified independently without their parent request type. "
        "If there is a request type without any sub-request type, then display only the request type. "
        "Do not display any null request type. "
        "For each classification, assign a score based on how well the content matches the key attributes relevant to these request types and sub-request types. "
        "Prioritize context and the overall primary intent over isolated keywords. If multiple request types are present, determine the primary one based on "
        "the main action described. Classify and rank the email content by identifying the primary intent first and then secondary intents. "
        "Provide a confidence score for each classification and an explanation for why it was selected. "
        "Ensure that the response is formatted as a structured JSON object without any additional explanations, notes, or commentary. "
        "The response should include the following fields: "
        "{request_type, sub_request_type, confidence, matched_attributes, extracted_sentences} for all classifications and also extract primary_classification. "
        "Include all classified request and sub-request types in the response. "
        "The response format should strictly adhere to the following structure:\n\n"
        "{\n"
        "  \"primary_classification\": {\n"
        "    \"request_type\": \"\",\n"
        "    \"sub_request_type\": \"\",\n"
        "    \"confidence\": \"0.92\",\n"
        "    \"matched_attributes\": [\"\", \"\"],\n"
        "    \"extracted_sentences\": [\"\"]\n"
        "  },\n"
        "  \"classifications\": [\n"
        "    {\n"
        "      \"request_type\": \"\",\n"
        "      \"sub_request_type\": \"\",\n"
        "      \"confidence\": \"0.81\",\n"
        "      \"matched_attributes\": [\"\", \"\"],\n"
        "      \"extracted_sentences\": [\"\"]\n"
        "    },\n"
        "    {\n"
        "      \"request_type\": \"\",\n"
        "      \"sub_request_type\": \"\",\n"
        "      \"confidence\": \"0.74\",\n"
        "      \"matched_attributes\": [\"\", \"\"],\n"
        "      \"extracted_sentences\": [\"\"]\n"
        "    }\n"
        "  ]\n"
        "}\n\n"
        f"Rules: {json.dumps(rules, indent=2)}\n\n"
        f"Email Body:\n{email_body}\n\n"
        f"Attachment Content:\n{attachment_content}"
    )
    
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

    try:
        # Extracting the nested "content" field from "message"
        response_text = response.json()["message"]["content"]
        
        # Extract only the JSON part using regular expression
        json_response = re.search(r'(\{.*\})', response_text, re.DOTALL)
        if json_response:
            parsed_json = json.loads(json_response.group(1))
            return parsed_json
        else:
            return {"error": "Invalid JSON response format"}

    except KeyError:
        return {"error": "Invalid response structure"}