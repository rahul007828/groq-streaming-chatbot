import os
import tiktoken
from dotenv import load_dotenv
from groq import Groq


# ============================================================
# 1. LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("ERROR: GROQ_API_KEY was not found in .env")
    exit()


# ============================================================
# 2. CREATE GROQ CLIENT
# ============================================================

client = Groq(api_key=api_key)


# ============================================================
# 3. TOKENIZER
# ============================================================

encoding = tiktoken.get_encoding("cl100k_base")


# ============================================================
# 4. CONFIGURATION
# ============================================================

MODEL = "openai/gpt-oss-20b"

# Our own learning/project context budget
MAX_CONTEXT_TOKENS = 1000

# Maximum response size
MAX_OUTPUT_TOKENS = 300


# Current Groq pricing for GPT-OSS 20B
# Input:  $0.075 per 1 million tokens
# Output: $0.30  per 1 million tokens

INPUT_PRICE_PER_MILLION = 0.075
OUTPUT_PRICE_PER_MILLION = 0.30


# ============================================================
# 5. CONVERSATION MEMORY
# ============================================================

messages = []

conversation_summary = ""


# ============================================================
# 6. COUNT TOKENS IN MESSAGES
# ============================================================

def count_message_tokens(messages):

    text = ""

    for message in messages:

        text += message["content"] + " "

    return len(encoding.encode(text))


# ============================================================
# 7. COUNT TOTAL CONTEXT TOKENS
# ============================================================

def count_context_tokens(messages, summary):

    total = count_message_tokens(messages)

    if summary:
        total += len(encoding.encode(summary))

    return total


# ============================================================
# 8. CALCULATE API COST
# ============================================================

def calculate_cost(input_tokens, output_tokens):

    input_cost = (
        input_tokens / 1_000_000
    ) * INPUT_PRICE_PER_MILLION

    output_cost = (
        output_tokens / 1_000_000
    ) * OUTPUT_PRICE_PER_MILLION

    total_cost = input_cost + output_cost

    return input_cost, output_cost, total_cost


# ============================================================
# 9. SUMMARIZE OLD CONVERSATION
# ============================================================

def summarize_messages(old_messages, existing_summary):

    old_text = ""

    for message in old_messages:

        old_text += (
            f"{message['role']}: "
            f"{message['content']}\n"
        )

    summary_prompt = f"""
You are summarizing an AI chatbot conversation.

Existing summary:
{existing_summary}

Older conversation:
{old_text}

Create a concise summary that preserves important
information needed to continue the conversation.

Keep:

- User identity
- User preferences
- Important facts
- User goals
- Important topics
- Important decisions

Do not invent information.

Keep the summary short.
"""

    response = client.chat.completions.create(

        model=MODEL,

        messages=[
            {
                "role": "user",
                "content": summary_prompt
            }
        ],

        max_completion_tokens=200,

        stream=False
    )

    return response.choices[0].message.content


# ============================================================
# 10. MANAGE CONTEXT
# ============================================================

def manage_context(messages, conversation_summary):

    while (

        count_context_tokens(
            messages,
            conversation_summary
        )

        > MAX_CONTEXT_TOKENS

        and len(messages) >= 2

    ):

        print("\n[Context limit reached]")

        print("[Summarizing older messages...]")

        # Take the oldest two messages

        old_messages = messages[:2]

        # Create/update summary

        conversation_summary = summarize_messages(

            old_messages,

            conversation_summary

        )

        # Remove those old messages

        del messages[:2]

        # Calculate current context size

        current_tokens = count_context_tokens(

            messages,

            conversation_summary

        )

        print("[Older messages summarized]")

        print(
            f"[Current context tokens: "
            f"{current_tokens}]"
        )

    return messages, conversation_summary


# ============================================================
# 11. START CHATBOT
# ============================================================

print("========================================")

print("       GROQ STREAMING CHATBOT")

print("========================================")

print("Model:", MODEL)

print("Chatbot started!")

print("Type 'exit' to stop.\n")


# ============================================================
# 12. MAIN CHAT LOOP
# ============================================================

while True:

    user_message = input("You: ")

    # --------------------------------------------------------
    # EXIT
    # --------------------------------------------------------

    if user_message.lower() == "exit":

        print("Goodbye!")

        break

    # --------------------------------------------------------
    # ADD USER MESSAGE
    # --------------------------------------------------------

    messages.append({

        "role": "user",

        "content": user_message

    })

    # --------------------------------------------------------
    # MANAGE CONTEXT
    # --------------------------------------------------------

    messages, conversation_summary = manage_context(

        messages,

        conversation_summary

    )

    # --------------------------------------------------------
    # BUILD MESSAGES SENT TO MODEL
    # --------------------------------------------------------

    model_messages = []

    # Add conversation summary if available

    if conversation_summary:

        model_messages.append({

            "role": "system",

            "content":
                "Summary of the earlier conversation:\n\n"
                + conversation_summary

        })

    # Add current conversation messages

    model_messages.extend(messages)

    # --------------------------------------------------------
    # COUNT INPUT TOKENS
    # --------------------------------------------------------

    input_tokens = count_context_tokens(

        messages,

        conversation_summary

    )

    print()

    print(f"[Input tokens: {input_tokens}]")

    print(
        f"[Maximum output tokens: "
        f"{MAX_OUTPUT_TOKENS}]"
    )

    # --------------------------------------------------------
    # CALL GROQ API
    # --------------------------------------------------------

    try:

        response = client.chat.completions.create(

            model=MODEL,

            messages=model_messages,

            max_completion_tokens=MAX_OUTPUT_TOKENS,

            stream=True

        )

        # ----------------------------------------------------
        # STREAM RESPONSE
        # ----------------------------------------------------

        print("Assistant: ", end="", flush=True)

        assistant_message = ""

        for chunk in response:

            text = (
                chunk.choices[0].delta.content
                or ""
            )

            print(
                text,
                end="",
                flush=True
            )

            assistant_message += text

        print()

        # ----------------------------------------------------
        # COUNT OUTPUT TOKENS
        # ----------------------------------------------------

        output_tokens = len(

            encoding.encode(
                assistant_message
            )

        )

        # ----------------------------------------------------
        # SAVE ASSISTANT MESSAGE
        # ----------------------------------------------------

        messages.append({

            "role": "assistant",

            "content": assistant_message

        })

        # ----------------------------------------------------
        # CALCULATE TOTAL TOKENS
        # ----------------------------------------------------

        total_tokens = (

            input_tokens
            + output_tokens

        )

        # ----------------------------------------------------
        # CALCULATE COST
        # ----------------------------------------------------

        input_cost, output_cost, total_cost = (
            calculate_cost(
                input_tokens,
                output_tokens
            )
        )

        # ----------------------------------------------------
        # DISPLAY TOKEN INFORMATION
        # ----------------------------------------------------

        print()

        print("----------------------------------------")

        print(
            f"Input tokens:  {input_tokens}"
        )

        print(
            f"Output tokens: {output_tokens}"
        )

        print(
            f"Total tokens:  {total_tokens}"
        )

        print("----------------------------------------")

        # ----------------------------------------------------
        # DISPLAY COST INFORMATION
        # ----------------------------------------------------

        print(
            f"Input cost:    ${input_cost:.8f}"
        )

        print(
            f"Output cost:   ${output_cost:.8f}"
        )

        print(
            f"Total cost:    ${total_cost:.8f}"
        )

        print("----------------------------------------")

        # ----------------------------------------------------
        # DISPLAY STORED CONVERSATION TOKENS
        # ----------------------------------------------------

        stored_tokens = count_context_tokens(

            messages,

            conversation_summary

        )

        print(
            f"[Stored conversation tokens: "
            f"{stored_tokens}]"
        )

        print()

    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as e:

        print("\n")

        print("========================================")

        print("ERROR")

        print("========================================")

        print(
            f"{type(e).__name__}: {str(e)}"
        )

        print("========================================")

        print()
