import os
import streamlit as st
from dotenv import load_dotenv
import anthropic

load_dotenv()

# PAGE CONFIG
st.set_page_config(
    page_title="Apple 10-K Analyst",
    page_icon="📈",
    layout="centered"
)


def get_api_key():

    key = os.getenv("ANTHROPIC_API_KEY")

    if not key:
        st.error("No Anthropic API key found.")
        st.stop()

    return key


@st.cache_data
def load_context(filepath):

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read()

    except FileNotFoundError:
        return ""


def build_system_prompt(context):

    return f"""
You are a financial analyst AI assistant.

Answer ONLY using the Apple 10-K filing below.

Rules:
- Be precise
- Use step-by-step reasoning
- Do not hallucinate
- If answer is missing from filing, say so

APPLE 10-K FILING:

{context}
"""


def get_response(messages, system_prompt, api_key):

    client = anthropic.Anthropic(api_key=api_key)

    conversation = ""

    for msg in messages:
        conversation += f"{msg['role']}: {msg['content']}\n"

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": conversation
            }
        ]
    )

    return response.content[0].text


# SESSION STATE
if "messages" not in st.session_state:
    st.session_state.messages = []


# LOAD DATA
api_key = get_api_key()
context = load_context("data/context.txt")
system_prompt = build_system_prompt(context)


# SIDEBAR
with st.sidebar:

    st.title("📈 Apple 10-K Analyst")

    st.markdown("""
Ask questions about Apple's annual filing.

### Example Questions
- What were Apple's major revenue sources?
- What risks did Apple mention?
- How much cash does Apple hold?
- What are Apple's future challenges?
""")

    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.caption(f"Messages in history: {len(st.session_state.messages)}")


# MAIN UI
st.title("Apple 10-K Q&A")

st.caption("Answers grounded in Apple's annual filing")

if not context:
    st.warning("Please add data/context.txt")
    st.stop()


# DISPLAY OLD MESSAGES
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# CHAT INPUT
if user_input := st.chat_input("Ask a question about Apple's 10-K..."):

    # SHOW USER MESSAGE
    with st.chat_message("user"):
        st.write(user_input)

    # SAVE USER MESSAGE
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # ASSISTANT RESPONSE
    with st.chat_message("assistant"):

        with st.spinner("Analysing filing..."):

            try:

                response_text = get_response(
                    st.session_state.messages,
                    system_prompt,
                    api_key
                )

                st.write(response_text)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response_text
                })

            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")