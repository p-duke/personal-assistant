import json
from pathlib import Path

from ollama import Client

from chat.schemas import ChatResponseSchema
from task_manager.services import create_task, complete_task
from task_manager.models import Task


def handle_intent(parsed_result):
    context = {}

    if parsed_result.intent == "create_task":
        new_task = create_task(
            title=parsed_result.task.title,
            priority=parsed_result.task.priority,
            due_date=parsed_result.task.due_date,
            estimated_duration=parsed_result.task.estimated_duration,
        )

        context = {
            "created": True,
            "task_id": str(new_task.id),
            "title": new_task.title,
            "priority": new_task.priority,
            "due_date": new_task.due_date,
            "duration": new_task.estimated_duration or "N/A",
        }

    if parsed_result.intent == "complete_task":
        task_data = parsed_result.task
        print("complete task intent", parsed_result)

        if task_data and task_data.task_id:
            task = complete_task(task_data.task_id)
            context = {
                "completed": True,
                "task_id": str(task.id),
                "title": task.title,
                "priority": task.priority,
                "due_date": task.due_date,
            }
        if task_data and task_data.task_identifier:
            task = Task.objects.filter(title__icontains=task_data.task_identifier).first()
            complete_task(task.id)
            context = {
                "completed": True,
                "task_id": str(task.id),
                "title": task.title,
                "priority": task.priority,
                "due_date": task.due_date,
            }

    print(f"handle_intent context: {context}")
    return context

def parse_message(message: str) -> ChatResponseSchema:
    prompt_template = load_prompt("detect_intent_extract_data.txt")
    prompt = prompt_template.format(user_message=message)
    raw_output = call_ollama(prompt)
    print(f"raw_output {raw_output}")

    if raw_output is None:
        return ChatResponseSchema(intent="error", task=None, error="LLM call failed")

    parsed_data = validate_and_parse_llm_resp(raw_output)
    print(f"parsed_data {parsed_data}")
    validated_response = ChatResponseSchema(**parsed_data)
    print(f"validated_response {validated_response}")

    return validated_response

def load_prompt(template_name: str) -> str:
    base_dir = Path(__file__).resolve().parent
    prompt_path = base_dir / "prompts" / template_name

    with open(prompt_path, "r") as f:
        return f.read()


def call_ollama(prompt: str) -> str | None:
    MODEL_NAME = "qwen2.5:14b-instruct-q4_K_M"
    client = Client(host="http://localhost:11434")

    try:
        response = client.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.message.content
    except Exception as e:
        raise Exception(f"Ollama error: {str(e)}")


def validate_and_parse_llm_resp(raw_text: str) -> dict:
    """
    Parse raw LLM text into a JSON dictionary suitable for ChatResponseSchema.

    On JSON errors, returns a dict the schema can accept:
    {
        "intent": "error",
        "data": None,
        "error": "reason..."
    }
    """
    text = raw_text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "intent": "error",
            "data": None,
            "error": f"Invalid JSON from LLM:\n{text[:200]}"
        }
