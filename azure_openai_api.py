import requests

def ask_azure_openai(prompt, deployment_name, api_key, endpoint_base):
    endpoint = f"{endpoint_base}/openai/deployments/{deployment_name}/chat/completions?api-version=2023-05-15"

    headers = {
        "Content-Type": "application/json",
        "api-key": "2MTbbBLRpmpNv7sP6UJYF3kM3CuUhbVUL1Dad0mYzUoeVPuBvL8GJQQJ99BFAC77bzfXJ3w3AAABACOGUO8O"
    }

    data = {
        "messages": [
            {"role": "system", "content": "You are a helpful career coach assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 300,
        "temperature": 0.7
    }

    response = requests.post(endpoint, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"


