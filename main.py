import argparse
import requests
import json

from prompts import system_prompt
from call_functions import available_functions, call_function
from functions.get_files_info import get_files_info

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2"
WORKING_DIRECTORY = "calculator"

def main():
    print("Hello from aiagent!")

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": args.user_prompt},
        ],
        "tools": available_functions,
        "tool_choice": "auto",
        "stream": False,
    }

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code != 200:
        raise RuntimeError(f"Ollama request failed: {response.text}")

    data = response.json()
    message = data["message"]

    # Ollama provides token counts too
    usage = data.get("usage", {})
    prompt_tokens = usage.get("prompt_tokens", 0)
    response_tokens = usage.get("completion_tokens", 0)

    if args.verbose:
        print(
            f"User prompt: {args.user_prompt}\n"
            f"Prompt tokens: {prompt_tokens}\n"
            f"Response tokens: {response_tokens}\n"
        )
    
     # Tool calling
    tool_calls = message.get("tool_calls", [])
    tool_results = []

    if tool_calls:
        for tool_call in tool_calls:
            tool_result = call_function(
                tool_call,
                WORKING_DIRECTORY,
                args.verbose
            )

            if not tool_result:
                raise RuntimeError("Tool returned empty response")

            if "content" not in tool_result:
                raise RuntimeError("Tool response missing content")

            tool_results.append(tool_result)

            if args.verbose:
                print(f"-> {tool_result['content']}")
    else:
        print(f"Response:\n{message.get('content','')}")
        
    #print(f"Response:\n{text}")

if __name__ == "__main__":
    main()