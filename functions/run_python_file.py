import os 
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_working_directory = os.path.abspath(working_directory)
    abs_path = os.path.abspath(os.path.join(abs_working_directory, file_path))

    if not abs_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_path):
        return f'Error: File "{file_path}" not found.'
    if not abs_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        if len(args) >= 1:
            
            process = subprocess.run(["python3",abs_path] + args, timeout=30, capture_output=True, text=True)
        else:
            process = subprocess.run(["python3",abs_path], timeout=30, capture_output=True, text=True)
        
        if process.returncode !=0:
            return f'STDOUT: {process.stdout}\nSTDERR: {process.stderr}\nProcess exited with code {process.returncode}'
        if not process.stdout and not process.stderr:
            return "No output produced."

        return f'STDOUT: {process.stdout}\nSTDERR: {process.stderr}'

    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name='run_python_file',
    description='runs a python file in the specified path, constrained to the working directory',
    parameters=types.Schema(
        type= types.Type.OBJECT,
        properties={
            'file_path': types.Schema(
                type= types.Type.STRING,
                description='the path to the python file, relative to the working directory, required argument'
            ),
            'args': types.Schema(
                type= types.Type.ARRAY,
                items= types.Schema(
                    type= types.Type.STRING
                ),
                description="arguments that will be passed to the python file,IT'S AN OPTIONAL ARGUMENT"
            )
        }
    )
)
