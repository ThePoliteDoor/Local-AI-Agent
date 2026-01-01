import argparse
import requests
import json

from prompts import system_prompt
from call_functions import available_functions, call_function

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5"
WORKING_DIRECTORY = "calculator"

def main():
    print("Hello from aiagent!")

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    for _ in range(20):
        payload = {
            "model": MODEL,
            "messages": messages,
            "tools": available_functions,
            "tool_choice": "auto",
            "stream": False,
        }

        response = requests.post(OLLAMA_URL, json=payload)
        if response.status_code != 200:
            raise RuntimeError(f"Ollama request failed: {response.text}")

        #storing messages
        data = response.json()
        message = data["message"]
        messages.append(message)

        # Ollama token counts
        #usage = data.get("usage", {})
        #prompt_tokens = usage.get("prompt_tokens", 0)
        #response_tokens = usage.get("completion_tokens", 0)

        if args.verbose:
            print(
                "\nLLM:", message.get("content", "")
                #f"User prompt: {args.user_prompt}\n"
                #f"Prompt tokens: {prompt_tokens}\n"
                #f"Response tokens: {response_tokens}\n"
            )
        
        # Tool requests?
        tool_calls = message.get("tool_calls", [])
        if not tool_calls:
            # Final answer — no more tools requested
            print("\nFinal answer:\n")
            print(message.get("content", ""))
            return
        
        tool_messages = []
        for tool_call in tool_calls:
            tool_result = call_function(
                tool_call,
                WORKING_DIRECTORY,
                args.verbose
            )

            if not tool_result or "content" not in tool_result:
                raise RuntimeError("Invalid tool result")

            tool_messages.append(tool_result)

            if args.verbose:
                print(f"-> {tool_result['content']}")

        # Feed tool results back to the model
        for tool in tool_messages:
            messages.append({
                "role": "tool",
                "tool_name": tool["tool_name"],
                "content": json.dumps(tool["content"])
            })

    # If we get here, we hit the iteration limit
    print("Error: Agent did not finish after 20 iterations")
    exit(1)
        

if __name__ == "__main__":
    main()