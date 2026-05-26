from anthropic import Anthropic

client = Anthropic(
    api_key="your_api_key"
)


friendly_prompt = """
You are a friendly AI assistant.
Always answer casually and encouragingly.
"""

strict_prompt = """
You are a strict technical assistant.
Give short, direct, professional answers only.
"""

funny_prompt = """
You are a funny AI assistant.
Answer everything with humor while still being helpful.
"""


question = input("Ask something: ")


if question.strip() == "":
    print("Please ask a valid question.")
    exit()


def ask_ai(system_prompt, label):
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=300,
        system=system_prompt,
        messages=[
            {"role": "user", "content": question}
        ]
    )

    print(f"\n--- {label} RESPONSE ---")
    print(response.content[0].text)




ask_ai(friendly_prompt, "FRIENDLY")
ask_ai(strict_prompt, "STRICT")
ask_ai(funny_prompt, "FUNNY")
