from google.generativeai import client

# Replace with your actual Google API key
client.api_key = "YOUR_GOOGLE_API_KEY"

models = client.list_models()
print("Available models:")
for model in models:
    print(model)
