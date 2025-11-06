import os 
from google.genai import types

def write_file(working_directory, file_path, content):
    abs_working_directory = os.path.abspath(working_directory)
    abs_path = os.path.abspath(os.path.join(abs_working_directory, file_path))

    if not abs_path.startswith(abs_working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    elif not os.path.exists(os.path.dirname(abs_path)):
        os.makedirs(os.path.dirname(abs_path))
    
    try:
        with open(abs_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="it can writes or overwrite content in the specified file path, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description='the file path to write content, relative to the working directory, required argument'
            ),
            'content': types.Schema(
                type=types.Type.STRING,
                description='the content that will be written to the file, it can be an empty string')
        }
    )
)
