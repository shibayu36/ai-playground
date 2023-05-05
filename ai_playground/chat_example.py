from functools import reduce
import os
import openai
import tiktoken

openai.api_key = os.environ["OPENAI_API_KEY"]

encoding = tiktoken.get_encoding("cl100k_base")


def get_total_token_count(messages):
    return reduce(
        lambda acc, message: acc + len(encoding.encode(message["content"])), messages, 0
    )


messages = [
    {"role": "system", "content": "関西弁で話して"},
    {"role": "system", "content": "発言の最後に「知らんけど。」をつけて"},
]


while True:
    user_message = input("You: ")
    messages.append({"role": "user", "content": user_message})

    print("Assistant: ", end="", flush=True)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.5,
        stream=True,
    )
    current_message = ""
    for chunk in response:
        delta_content = chunk["choices"][0]["delta"].get("content", "")
        print(delta_content, end="", flush=True)
        current_message += delta_content
    print()

    messages.append({"role": "assistant", "content": current_message})

    total_token_count = get_total_token_count(messages)
    print(f"Total token count: {total_token_count}")

    # Delete old messages if messages are about to exceed the limit
    while total_token_count > 2500:
        print("Delete old context")
        del messages[2]
        total_token_count = get_total_token_count(messages)
        print(f"Total token count: {total_token_count}")
