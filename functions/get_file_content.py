import os

from functions.config import MAX_CHARS
from google.genai import types


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path.",
            ),
        },
    ),
)


def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    abs_file_path = os.path.abspath(full_path)
    abs_working_directory = os.path.abspath(working_directory)

    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(abs_file_path, "r") as f:
            try:
                file_size = os.path.getsize(abs_file_path)
            except Exception as e:
                return f"Error: Failed to get {file_path} size"

            try:
                if file_size > MAX_CHARS:
                    file_content_string = (
                        f.read(MAX_CHARS)
                        + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                    )
                else:
                    file_content_string = f.read()
            except Exception as e:
                return f"Error: Failed to read {file_path} content"

            return file_content_string
    except Exception as e:
        return f"Error: Failed to open {file_path}"
