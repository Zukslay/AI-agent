import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types  
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    load_dotenv()
    
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    
    user_prompt = None
    for arg in sys.argv[1:]:
        if not arg.startswith("--") and not arg.startswith('-'):
            user_prompt = arg
            break
    if not user_prompt:
        print("Error: cero arguments provided")
        exit(1)
    
    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions],
                                           system_instruction=system_prompt))
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if not response.function_calls:
        print(response.text)
        return response.text

    for function in response.function_calls:
        function_call_result = call_function(function, verbose)
        if not function_call_result.parts[0].function_response.response:
            raise Exception("Error: missing function_call_result.parts[0].function_response.response")
        
        print(f"-> {function_call_result.parts[0].function_response.response}")


    


if __name__ == "__main__":
    main()
