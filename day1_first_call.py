import os
from dotenv import load_dotenv
import anthropic


def setup():
    load_dotenv()

    client = anthropic.Anthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )

    return client


def make_api_call(client):
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "What is Apple's primary business? Answer in two sentences."
            }
        ]
    )

    return response


def extract_answer(response):
    answer = response.content[0].text
    return answer


def print_usage(response):
    print("Token usage:")
    print(f"Input tokens: {response.usage.input_tokens}")
    print(f"Output tokens: {response.usage.output_tokens}")


def main():
    client = setup()
    response = make_api_call(client)
    answer = extract_answer(response)

    print("Model response:")
    print(answer)
    print()

    print_usage(response)


if __name__ == "__main__":
    main()