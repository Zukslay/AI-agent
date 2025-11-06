import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types  
from prompts import system_prompt
from call_function import available_functions, call_function
from config import MAX_LOOP

def main():
    #leer variables de entorno y obtener cliente gemini
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    #chequear si hay verbose y obtener el prompt del usuario
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    user_prompt = get_prompt()
    if not user_prompt:
        print("Error: zero arguments provided")
        exit(1)
    
    #configuracion de generate_content
    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    ai_model = "gemini-2.0-flash-001"
    ai_config = types.GenerateContentConfig(tools=[available_functions],
                                           system_instruction=system_prompt)
    
    for _ in range(MAX_LOOP):
        try:
            response = client.models.generate_content(
                model=ai_model,
                contents=messages,
                config=ai_config)
        except Exception as e:
            raise Exception(f"error: {e}")

        for candidate in response.candidates:
            messages.append(candidate.content)

        if verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        if response.function_calls is not None:
            try:
                for function in response.function_calls:
                    function_call_result = call_function(function, verbose)
                    result = function_call_result.parts[0].function_response.response
                    if not result:
                        raise Exception("Error: missing function_call_result.parts[0].function_response.response")
                    if verbose:
                        print(f"-> {result}")
                    messages.append(types.Content(role='user',
                                                  parts=[types.Part(text=result['result'])]))
            except Exception as e:
                raise Exception(f"error: {e}")
        
        if response.text and response.function_calls is None:
            print(response.text)
            break

def get_prompt():
    for arg in sys.argv[1:]:
        if not arg.startswith("--") and not arg.startswith('-'):
            prompt = arg
            return prompt
    return None


if __name__ == "__main__":
    main()
