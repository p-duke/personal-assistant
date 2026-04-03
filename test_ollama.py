#!/usr/bin/env python3
"""
One-off Ollama Python SDK example for local models
"""

from ollama import Client

client = Client(
  host='http://localhost:11434',
)
response = client.chat(model='qwen2.5:14b-instruct-q4_K_M', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])

print(response.message.content)
