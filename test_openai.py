import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()                                    # reads .env
client = OpenAI()                                # picks up OPENAI_API_KEY automatically

resp = client.chat.completions.create(
    model="gpt-4o-mini-2024-07-18",              # version-pinned for reproducibility
    messages=[{"role": "user",
               "content": "In one sentence: what is the capital of Nigeria?"}],
    temperature=0,
)
print("RESPONSE:", resp.choices[0].message.content)
print("MODEL:", resp.model)
print("TOKENS:", resp.usage.total_tokens)
