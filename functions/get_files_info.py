import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    """
    Get detailed info about the contents of a directory safely within a working directory.

    Args:
        working_directory (str): Base working directory
        directory (str): Target subdirectory relative to working_directory

    Returns:
        str: Formatted string listing the contents of the directory, or an error message prefixed with 'Error:'
    """
    try:
        # Get absolute path of working directory
        working_dir_abs = os.path.abspath(working_directory)

        # Resolve target directory path
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # Ensure target is inside working directory
        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check if target path exists and is a directory
        if not os.path.exists(target_dir):
            return f'Error: "{directory}" does not exist'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        # List files with detailed info
        items = os.listdir(target_dir)
        if not items:
            return f'The directory "{directory}" is empty.'

        result_lines = []
        for item in items:
            item_path = os.path.join(target_dir, item)
            size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            # Format as bullet list
            result_lines.append(f'- {item}: file_size={size} bytes, is_dir={is_dir}')

        return "\n".join(result_lines)

    except Exception as e:
        return f"Error: {str(e)}"


# Scheme for LLM
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
