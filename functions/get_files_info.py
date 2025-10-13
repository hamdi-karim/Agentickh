import os


def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    abs_full_path = os.path.abspath(full_path)
    abs_working_directory = os.path.abspath(working_directory)

    if not abs_full_path.startswith(abs_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(abs_full_path):
        return f'Error: "{directory}" is not a directory'

    try:
        contents = os.listdir(abs_full_path)
    except Exception as e:
        return f"Error: Failed to list directory contents: {e}"

    lines = []

    for item in contents:
        item_path = os.path.join(abs_full_path, item)
        try:
            is_dir = os.path.isdir(item_path)
            file_size = os.path.getsize(item_path)
            lines.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")
        except Exception as e:
            return f"Error: Failed to get info for '{item}': {e}"

    return "\n".join(lines)
