import requests
import json
import os

system_msg = """You are a senior essay writer."""

def chat_gpt(prompt, model="gpt-3.5-turbo", system_msg=system_msg):
    url = f"{os.environ.get('OPENAI_URL')}/v1/chat/completions"
    if os.environ.get("APP_ENV") == "development":
        proxy = {
            'http': os.environ.get("PROXY_FOR_OPENAI"),
            'https': os.environ.get("PROXY_FOR_OPENAI")
        }
    else:
        proxy = None
    
    payload = {
        "model": model,
        "temperature": 0.7,
        "messages": [
            {
                "role": "system",
                "content": system_msg
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY')}",
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(payload), proxies=proxy)
    
    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    
    else:
        return f"Request failed with status code {response.status_code}: {response.text}"