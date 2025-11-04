import os 
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    abs_working_directory = os.path.abspath(working_directory)
    abs_path = os.path.abspath(os.path.join(abs_working_directory, file_path))

    if not abs_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    elif not os.path.exists(abs_path):
        return f'Error: File "{file_path}" not found.'
    elif not abs_path.endswith(".py"):
        f'Error: "{file_path}" is not a Python file.'
    
    try:
        if len(args) >= 1:
            process = subprocess.run(args, timeout=30, capture_output=True)
        else:
            process = subprocess.run(abs_path, timeout=30, capture_output=True)
        
        if not process.stdout:
            return "No output produced."
        if process.returncode !=0:
            return f'STDOUT: {process.stdout}\nSTDERR: {process.stderr}\nProcess exited with code {process.returncode}'

        return f'STDOUT: {process.stdout}\nSTDERR: {process.stderr}'

    except Exception as e:
        return f"Error: executing Python file: {e}"
