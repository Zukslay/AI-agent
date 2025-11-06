from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)

dispatch = {"get_file_content": get_file_content,
            "get_files_info": get_files_info,
            "write_file": write_file,
            "run_python_file": run_python_file}

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    work_arg = {"working_directory": "./calculator"}
    some_args = dict(**work_arg, **function_call_part.args)
    
    func = dispatch.get(function_call_part.name)
    if not func:
        return types.Content(
            role="tool",
            parts=[types.Part.from_function_response(
                name=function_call_part.name,
                response={"error": f"Unknown function: {function_call_part.name}"}
            )],
        )
    try:
        
        result = func(**some_args)
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={"result": result},
        )
    ],
)
    except Exception as e:
        print(f'Error: {e}')
        return types.Content(
            role="tool",
            parts=[types.Part.from_function_response(
                name=function_call_part.name, response={"error": str(e)}
            )]
        )

    