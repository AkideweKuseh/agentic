# call_function.py
from google.genai import types
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.get_files_info import get_files_info, schema_get_files_info

# All available tools for Gemini
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ],
)

# Map function names to actual Python callables
function_map = {
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
    "get_files_info": get_files_info,
}

def call_function(function_call, verbose=False):
    """
    Call one of the available functions based on the FunctionCall object
    and return a types.Content object with the result.
    """
    function_name = function_call.name or ""

    # Print function being called
    if verbose:
        print(f"Calling function: {function_name}({function_call.args})")
    else:
        print(f" - Calling function: {function_name}")

    # Check if function exists
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # Copy and modify args
    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = "./calculator"

    # Call the function
    function_result = function_map[function_name](**args)

    # Wrap the result in a Content object
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
