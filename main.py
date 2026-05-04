import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function


def generate_response(client, messages):
    """
    Calls Gemini API and returns the response.
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
            temperature=0
        ),
    )

    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    return response


def main():
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found")

    # Parse CLI arguments
    parser = argparse.ArgumentParser(description="Chatbot Agent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # Initialize Gemini client
    client = genai.Client(api_key=api_key)

    # Conversation history
    messages = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]

    # 🔁 Agent loop
    for iteration in range(20):
        if args.verbose:
            print(f"\n--- Iteration {iteration + 1} ---")

        response = generate_response(client, messages)

        # Verbose token info
        if args.verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

        # 🧠 Add model responses (candidates) to history
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        function_results = []

        # 🔧 Handle function calls
        if response.function_calls:
            for function_call in response.function_calls:
                result = call_function(function_call, verbose=args.verbose)

                if not result.parts:
                    raise RuntimeError("No parts returned from function call")

                part = result.parts[0]
                func_response = part.function_response

                if func_response is None or func_response.response is None:
                    raise RuntimeError("Invalid function response")

                function_results.append(part)

                if args.verbose:
                    print(f"-> Tool result: {func_response.response}")

            # 🧾 Add tool results to conversation
            messages.append(
                types.Content(role="user", parts=function_results)
            )

        else:
            # ✅ Final answer (no more tool calls)
            print("\nFinal Response:\n")
            print(response.text)
            return

    # ❌ Loop limit hit
    print("\nAgent stopped: reached max iterations without completing task.")
    exit(1)


if __name__ == "__main__":
    main()
