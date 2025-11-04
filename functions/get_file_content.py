import os

def get_file_content(working_directory, file_path):
    working_directory_path = os.path.abspath(working_directory)
    absolute_path = os.path.abspath(os.path.join(working_directory_path, file_path))
    
    if not absolute_path.startswith(working_directory_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(absolute_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(file_path, "r") as f:
            file_content_string = f.read(10000)
        
            append = ''
            if file_content_string == 10000:
                append = f'[...File "{file_path}" truncated at 10000 characters]'
            return file_content_string + append
    
    except Exception as e:
        return f'Error: {e}'
        
