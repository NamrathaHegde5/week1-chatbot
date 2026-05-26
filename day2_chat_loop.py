import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)


def load_context(filepath: str) -> str:
    """
    Reads the Apple 10-K text file and returns its contents as a string.
    """

    with open(filepath, "r", encoding="utf-8") as file:
        contents = file.read()

    return contents


def build_system_prompt(context: str) -> str:
    """
    Takes the 10-K text and wraps it in a system prompt.
    Returns the full prompt as a string.
    """

    return f"""
You are a financial analyst assistant for Apple Inc.

You must ONLY use information from the Apple 10-K filing provided below.

If the answer is not found in the filing, clearly say that the information is not available in the filing.

Quote all numbers exactly as written.

Think step by step before answering.

APPLE 10-K FILING:
{context}
"""


def chat(user_message: str, history: list, system_prompt: str) -> str:
    """
    Sends the user message to the API along with conversation history.
    """

    # STEP 1 — append user message to history

    history.append({
        "role": "user",
        "content": user_message
    })

    # STEP 2 — build messages list

    messages = []

    for msg in history:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    # STEP 3 — API call

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        system=system_prompt,
        messages=messages
    )

    # STEP 4 — extract assistant message

    assistant_message = ""

    for block in response.content:
        if block.type == "text":
            assistant_message += block.text

    # STEP 5 — append assistant message to history

    history.append({
        "role": "assistant",
        "content": assistant_message
    })

    # STEP 6 — return assistant message

    return assistant_message

def main():
    """
    Loads context and starts chat loop.
    """

    # STEP 1 — load context

    context = load_context("data/context.txt")

    # STEP 2 — build system prompt

    system_prompt = build_system_prompt(context)

    # STEP 3 — create empty history list

    history = []

    # STEP 4 — welcome message

    print("Apple 10-K Q&A — type quit to exit")
    print("-" * 40)

    while True:

        # STEP 5 — get user input

        user_input = input("\nYou: ").strip()

        # STEP 6 — handle empty input

        if not user_input:
            print("Please enter a question.")
            continue

        # STEP 7 — quit condition

        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        # STEP 8 — call chat()

        response = chat(user_input, history, system_prompt)

        # STEP 9 — print response

        print(f"\nAssistant: {response}")

        # STEP 10 — debug history length

        print(f"[Debug: {len(history)} messages in history]")


if __name__ == "__main__":
    main()