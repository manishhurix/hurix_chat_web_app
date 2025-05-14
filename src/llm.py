import os
import openai
import anthropic

def get_available_models():
    # Return available LLMs and versions
    return [
        {"provider": "OpenAI", "name": "ChatGPT", "versions": ["gpt-3.5-turbo", "gpt-4"]},
        {"provider": "Anthropic", "name": "Claude", "versions": ["claude-v1", "claude-2"]},
    ]

def chat_with_model(model, messages, files=None):
    # Call the selected LLM with message history and optional files
    # model: dict with provider, name, version
    # messages: list of dicts [{role, content}]
    # files: list of file contents (optional)
    provider = model["provider"]
    version = model["version"]
    context = "\n".join(files) if files else ""
    try:
        if provider == "OpenAI":
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            # Prepare OpenAI messages
            openai_messages = []
            if context:
                openai_messages.append({"role": "system", "content": f"Document context: {context}"})
            openai_messages += [{"role": m["role"], "content": m["content"]} for m in messages]
            response = client.chat.completions.create(
                model=version,
                messages=openai_messages,
                max_tokens=1024,
                temperature=0.7
            )
            return response.choices[0].message.content
        elif provider == "Anthropic":
            client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            # Prepare Anthropic messages
            prompt = ""
            if context:
                prompt += f"Document context: {context}\n"
            for m in messages:
                if m["role"] == "user":
                    prompt += f"Human: {m['content']}\n"
                else:
                    prompt += f"Assistant: {m['content']}\n"
            response = client.completions.create(
                model=version,
                max_tokens_to_sample=1024,
                prompt=prompt + "Assistant:"
            )
            return response.completion.strip()
        else:
            return "[Model not supported]"
    except Exception as e:
        return f"[LLM Error: {str(e)}]" 