import requests

api_key = ""

# Set the endpoint URL
endpoint = "https://api.openai.com/chat/gpt"

# Set the request headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Set the request body
data = {
    "text": "What is the weather like today?",
    "model": "text-davinci-002"
}

# Send the request
response = requests.post(endpoint, headers=headers, json=data)

# Print the response
print(response.json())
