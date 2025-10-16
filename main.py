import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
# Creating a new instance of Gemini Client
client = genai.Client(api_key=api_key)
model_name = "gemini-2.0-flash-001"


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

    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    # Always print the model's response text
    if len(response.function_calls) == 0:
        print(response.text)
    else:
        function_call_part = response.function_calls[0]
        function_call_result = call_function(function_call_part, verbose=verbose)

        # Validate the structure
        parts = function_call_result.parts
        if not parts or not hasattr(parts[0], "function_response"):
            raise Exception("Function call returned invalid content")

        if verbose:
            print(f"-> {parts[0].function_response.response}")

    # Print verbose info only if flag is set
    if verbose:
        print("\n--- VERBOSE OUTPUT ---")
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
