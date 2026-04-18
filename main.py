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
MAX_STEPS = 20


def main():
    # Extract args and check for --verbose
    args = sys.argv[1:]
    verbose = False

    if "--verbose" in args:
        verbose = True
        args.remove("--verbose")

    # Build the prompt string, use default if none provided
    if not args:
        prompt = "Say hello and mention this is a default prompt."
    else:
        prompt = " ".join(args)

    system_prompt = """
        You are a helpful AI coding agent working in the current repository.
        When asked about “the calculator”, assume it refers to files under ./calculator/.
        Typical files: ./calculator/main.py, ./calculator/pkg/calculator.py, ./calculator/pkg/render.py.
        Use tools to:
        1) list files (start with ./ and subdirs),
        2) read relevant files,
        3) execute python files when needed,
        4) then answer.

        Prefer making function calls before giving a final answer. Paths are relative to the working directory.
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

    for step in range(MAX_STEPS):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )

            # 1) Append assistant candidates immediately (keeps full trace)
            if getattr(response, "candidates", None):
                for cand in response.candidates:
                    if hasattr(cand, "content") and cand.content:
                        messages.append(cand.content)

            # 2) If the model requested tool calls, run them, append results, and continue.
            if getattr(response, "function_calls", None):
                for fc in response.function_calls:
                    function_call_result = call_function(fc, verbose=verbose)

                    parts = getattr(function_call_result, "parts", None)
                    if not parts or not hasattr(parts[0], "function_response"):
                        raise ValueError(
                            "Invalid function result: missing function_response in parts[0]"
                        )

                    if verbose:
                        fr = parts[0].function_response
                        print(
                            f"-> function_response (tool={getattr(fr, 'name', 'unknown')}): {getattr(fr, 'response', fr)}"
                        )

                    # Append tool result back as a *user* message so the model can continue reasoning
                    messages.append(types.Content(role="user", parts=parts))

                # IMPORTANT: let the model take another step before printing any text
                continue

            # 3) No tool calls this turn: if final text exists, print and stop.
            if getattr(response, "text", None):
                usage = getattr(response, "usage_metadata", None)
                if usage is None:
                    raise RuntimeError(
                        "Missing usage_metadata on response; request may have failed."
                    )

                print(f"Prompt tokens: {usage.prompt_token_count}")
                print(f"Response tokens: {usage.candidates_token_count}")
                print(response.text)

                if verbose:
                    print("\n--- VERBOSE OUTPUT ---")
                    print(f"Prompt: {prompt}")
                break

            # If neither function_calls nor text were provided, loop continues to next step.
        except Exception as e:
            # Per-iteration protection: log and continue to next step
            print(f"[WARN] Step {step+1} failed: {e}")
    else:
        print("Reached the maximum of 20 iterations without final text.")


if __name__ == "__main__":
    main()
