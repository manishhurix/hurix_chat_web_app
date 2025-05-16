import os
# Unset proxy environment variables to avoid OpenAI SDK errors
os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)

import openai
import anthropic
import logging

MAX_CONTEXT_CHARS = 12000  # ~3000-4000 tokens
MAX_HISTORY = 10

# Setup basic logger
logger = logging.getLogger("llm")
if not logger.hasHandlers():
    logging.basicConfig(level=logging.INFO)

def get_available_models():
    # Return available LLMs and versions
    return [
        # {"provider": "OpenAI", "name": "ChatGPT", "versions": ["gpt-3.5-turbo", "gpt-4"]},
        {"provider": "Anthropic", "name": "Claude", "versions": ["claude-2"]},
    ]

def chat_with_model(model, messages, files=None):
    # Call the selected LLM with message history and optional files
    # model: dict with provider, name, version
    # messages: list of dicts [{role, content}]
    # files: list of file contents (optional)
    provider = model["provider"]
    version = model["version"]
    context = "\n".join(files) if files else ""
    if context and len(context) > MAX_CONTEXT_CHARS:
        context = context[:MAX_CONTEXT_CHARS]
    if len(messages) > MAX_HISTORY:
        messages = messages[-MAX_HISTORY:]
    try:
        if provider == "OpenAI":
            logger.info(f"Calling OpenAI model: {version}")
            api_key = os.getenv("OPENAI_API_KEY")
            try:
                # Try new SDK (v1.x) style
                client = openai.OpenAI(api_key=api_key)
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
            except AttributeError:
                # Fallback for openai<1.0.0
                openai.api_key = api_key
                openai_messages = []
                if context:
                    openai_messages.append({"role": "system", "content": f"Document context: {context}"})
                openai_messages += [{"role": m["role"], "content": m["content"]} for m in messages]
                response = openai.ChatCompletion.create(
                    model=version,
                    messages=openai_messages,
                    max_tokens=1024,
                    temperature=0.7
                )
                return response["choices"][0]["message"]["content"]
        elif provider == "Anthropic":
            logger.info(f"Calling Anthropic Claude model: {version}")
            api_key = os.getenv("ANTHROPIC_API_KEY")
            client = anthropic.Anthropic(api_key=api_key)
            # Only support Claude v2 (messages API)
            anthropic_messages = []
            # Prepend document context to the last user message if context exists
            if context and messages and messages[-1]["role"] == "user":
                messages = messages.copy()
                messages[-1] = messages[-1].copy()
                messages[-1]["content"] = f"[Document context: {context}]\n\n" + messages[-1]["content"]
            # Only keep 'role' and 'content' for each message
            anthropic_messages += [
                {"role": m["role"], "content": m["content"]}
                for m in messages if "role" in m and "content" in m
            ]
            response = client.messages.create(
                model=version,
                max_tokens=1024,
                messages=anthropic_messages
            )
            # Claude 2 returns a list of content blocks; join text blocks
            if hasattr(response, "content"):
                if isinstance(response.content, list):
                    return "".join(
                        block.text for block in response.content if hasattr(block, "text")
                    )
                return str(response.content)
            return str(response)
        else:
            logger.error(f"Model provider not supported: {provider}")
            return "[Model not supported]"
    except Exception as e:
        logger.exception(f"LLM Error for provider {provider}, version {version}: {e}")
        return f"[LLM Error: {str(e)}]" 