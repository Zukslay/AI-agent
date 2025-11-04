from functions.run_python_file import run_python_file
def main():
    
    inputs = [[ "main.py", []],
               [ "main.py", ["3 + 5"]],
                 [ "tests.py", []],
                 [ "../main.py", []],
                 [ "nonexistent.py", []],
                 [ "lorem.txt", []]]
    
    for input in inputs:
        result = run_python_file("calculator", input[0], input[1])
        input[0] = "current directory" if input[0] == "." else input[0]
        print(f"Result for '{input[0]}' directory:")
        print(result)




if __name__ == "__main__":
    main()