import json
import re
from pathlib import Path

# from .models import ChatMessage  # Commented out since we don't use it yet
from ollama import Client

from chat.schemas import ChatResponseSchema


def load_prompt(template_name: str) -> str:
    base_dir = Path(__file__).resolve().parent
    prompt_path = base_dir / "prompts" / template_name

    with open(prompt_path, "r") as f:
        return f.read()


def call_ollama(prompt: str) -> str | None:
    MODEL_NAME = "qwen2.5:14b-instruct-q4_K_M"
    client = Client(host="http://localhost:11434")
    # Use the ollama library directly instead of HTTP requests
    # OLLAMA_MODEL = getattr(settings, "OLLAMA_MODEL", "qwen2.5:14b-instruct-q4_K_M")
    # Call Ollama model
    try:
        response = client.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract text content
        return response.message.content 
    except Exception as e:
        raise Exception(f"Ollama error: {str(e)}")

    # # Parse JSON
    # try:
    #     data: Any = json.loads(raw_text)
    # except json.JSONDecodeError as e:
    #     raise ValueError(f"LLM output was not valid JSON:\n{raw_text}") from e
    #


def parse_llm_json(raw_text: str) -> dict:
    """
    Safely parse JSON response from LLM.

    Args:
        raw_text: Raw text response from LLM

    Returns:
        Parsed dictionary

    Raises:
        ValueError: If parsing fails
    """

    # Clean the text first
    text = raw_text.strip()

    # Remove any markdown code blocks if present
    if text.startswith("```json"):
        text = text[7:]  # Remove ```json
    if text.endswith("```"):
        text = text[:-3]  # Remove ```

    # Try direct JSON parsing first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Common recovery: find JSON between first { and last }
    json_match = re.search(r"\{.*\}", text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass

    # If nothing works, raise a clear error
    raise ValueError(f"Failed to parse JSON from LLM response. Got: {repr(text[:200])}")


def parse_message(message: str) -> ChatResponseSchema:
    prompt_template = load_prompt("create_task.txt")
    prompt = prompt_template.format(user_message=message)
    raw_output = call_ollama(prompt)
    parsed_data = parse_llm_json(raw_output)
    validated_response = ChatResponseSchema(**parsed_data)

    return validated_response
