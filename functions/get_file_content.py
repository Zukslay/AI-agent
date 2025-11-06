import os
from config import MAX_CHAR 
from google.genai import types  

def get_file_content(working_directory, file_path):
    working_directory_path = os.path.abspath(working_directory)
    absolute_path = os.path.abspath(os.path.join(working_directory_path, file_path))
    
    if not absolute_path.startswith(working_directory_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(absolute_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(absolute_path, "r") as f:
            file_content_string = f.read(MAX_CHAR)
        
            append = ''
            if len(file_content_string) == MAX_CHAR:
                append = f'[...File "{file_path}" truncated at 10000 characters]'
            return file_content_string + append
    
    except Exception as e:
        return f'Error: {e}'
    
schema_get_file_content = types.FunctionDeclaration(
    name = "get_file_content",
    description = 'shows content file in the specified path, constrained to the working directory',
    parameters = types.Schema(
        type = types.Type.OBJECT,
        properties = {
            'file_path': types.Schema(
                type = types.Type.STRING,
                description = 'the file path to get content from, relative to the working directory, required argument'
            )
        }
    )
)
        
