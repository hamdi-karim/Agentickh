import os
import subprocess
import sys


def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    abs_full_path = os.path.abspath(full_path)
    abs_working_directory = os.path.abspath(working_directory)
    common = os.path.commonpath([abs_working_directory, abs_full_path])

    if common != abs_working_directory:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_full_path):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        completed_process = subprocess.run(
            [sys.executable, file_path, *args],
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30,
        )

    except Exception as e:
        return f"Error: executing Python file: {e}"

    stdout = completed_process.stdout or ""
    stderr = completed_process.stderr or ""

    if (
        stdout.strip() == ""
        and stderr.strip() == ""
        and completed_process.returncode == 0
    ):
        return "No output produced."

    parts = [f"STDOUT:{stdout}", f"STDERR:{stderr}"]
    if completed_process.returncode != 0:
        parts.append(f"Process exited with code {completed_process.returncode}")

    return "\n".join(parts)
