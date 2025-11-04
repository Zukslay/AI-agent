import os

def get_files_info(working_directory, directory="."):
    
    abs_working_directory = os.path.abspath(working_directory)
    abs_path = os.path.abspath(os.path.join(abs_working_directory, directory))
    

    if not abs_path.startswith(abs_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    elif os.path.isfile(abs_path):
        return f'Error: "{directory}" is not a directory'
    
    contents = os.listdir(abs_path)
     
    string_list_out = []
    for content in contents:
        try:
            content_path = "/".join([abs_path, content])
            string_list_out.append(f"- {content}: file_size={os.path.getsize(content_path)}, is_dir={not os.path.isfile(content_path)}")
        except Exception as e:
            return f"Error: {e}"
    
    return "\n".join(string_list_out)