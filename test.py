from google import genai
from settings import api_key
client = genai.Client(api_key=api_key)
for model in client.models.list():
    print(model.name)
