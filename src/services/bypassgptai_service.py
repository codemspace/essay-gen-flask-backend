import requests
import os
import time

headers = {
    "Content-Type": "application/json",
    "api-key": os.environ.get("BYPASSGPTAI_API_KEY")
}
    
def get_task_id(text):
    url = f"{os.environ.get("BYPASSGPTAI_URL")}/api/bypassgpt/v1/generate"
    body = {
        "input": text,
        "model_type": "Enhanced"
    }
    response = requests.post(url, json=body, headers=headers)
    print(response.json())
    task_id = response.json()["data"]["task_id"]
    return task_id
    
def get_humanized_text(text):
    url = f"{os.environ.get("BYPASSGPTAI_URL")}/api/bypassgpt/v1/retrieval"
    task_id = get_task_id(text)
    params = {
        "task_id": task_id
    }
    response = requests.get(url, headers=headers, params=params)
    humanized_text = response.json()["data"]["output"]
    while not humanized_text:
        time.sleep(2)
        response = requests.get(url, headers=headers, params=params)
        print(response.json())
        humanized_text = response.json()["data"]["output"]
    score = response.json()["data"]["check_result"]["summary"]["score"]
    if score < 100:
        humanized_text, score = get_humanized_text(text)
    return humanized_text, score