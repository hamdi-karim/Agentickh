import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
# Creating a new instance of Gemini Client
client = genai.Client(api_key=api_key)


def main():
    if len(sys.argv) < 2:
        print("ERROR - Usage: uv run main.py '<your prompt here>' [--verbose]")
        sys.exit(1)

    # Extract args and check for --verbose
    args = sys.argv[1:]
    verbose = False

    if "--verbose" in args:
        verbose = True
        args.remove("--verbose")

    # Build the prompt string
    prompt = " ".join(args)

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    # Always print the model's response text
    print(response.text)

    # Print verbose info only if flag is set
    if verbose:
        print("\n--- VERBOSE OUTPUT ---")
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
