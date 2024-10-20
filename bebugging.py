import openai

from _secrets import api_key

openai.api_key = api_key

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello! How can you assist me today?"}
    ]
)

print(response.choices[0].message['content'])
