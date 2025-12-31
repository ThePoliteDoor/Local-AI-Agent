import argparse
import requests

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"

def main():
    print("Hello from aiagent!")

    payload = {
        "model": MODEL,
        "prompt": args.user_prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code != 200:
        raise RuntimeError(f"Ollama request failed: {response.text}")

    data = response.json()
    text = data["response"]

    # Ollama provides token counts too
    prompt_tokens = data.get("prompt_eval_count", 0)
    response_tokens = data.get("eval_count", 0)

    if args.verbose:
        print(
            f"User prompt: {args.user_prompt}\n"
            f"Prompt tokens: {prompt_tokens}\n"
            f"Response tokens: {response_tokens}\n"
        )

    print(f"Response:\n{text}")

if __name__ == "__main__":
    main()