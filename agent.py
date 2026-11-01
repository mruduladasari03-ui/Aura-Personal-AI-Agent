import json
import os
from openai import OpenAI
from database import list_tasks, add_task, list_goals, add_goal, add_memory, list_memories

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

def get_client():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is missing. Add it to your .env file.")
    return OpenAI(api_key=key)

def tool_add_task(title: str, priority: str = "Medium", due_date: str = ""):
    add_task(title, priority, due_date)
    return {"success": True, "message": f"Added task: {title}"}

def tool_list_tasks():
    return [{"id": t[0], "title": t[1], "priority": t[2], "due_date": t[3], "status": t[4]} for t in list_tasks()]

def tool_add_goal(title: str, description: str = ""):
    add_goal(title, description)
    return {"success": True, "message": f"Saved goal: {title}"}

def tool_save_memory(content: str):
    add_memory(content)
    return {"success": True, "message": "Memory saved."}

def tool_get_memory():
    return [{"content": m[1]} for m in list_memories()]

TOOLS = [
    {"type": "function", "function": {"name": "add_task", "description": "Add a task to the user's task list.", "parameters": {"type": "object", "properties": {"title": {"type": "string"}, "priority": {"type": "string", "enum": ["Low", "Medium", "High"]}, "due_date": {"type": "string", "description": "Optional date in YYYY-MM-DD format"}}, "required": ["title"], "additionalProperties": False}}},
    {"type": "function", "function": {"name": "list_tasks", "description": "Show the user's current tasks.", "parameters": {"type": "object", "properties": {}, "additionalProperties": False}}},
    {"type": "function", "function": {"name": "add_goal", "description": "Save a goal for the user.", "parameters": {"type": "object", "properties": {"title": {"type": "string"}, "description": {"type": "string"}}, "required": ["title"], "additionalProperties": False}}},
    {"type": "function", "function": {"name": "save_memory", "description": "Save a stable preference or useful fact the user explicitly asks Aura to remember.", "parameters": {"type": "object", "properties": {"content": {"type": "string"}}, "required": ["content"], "additionalProperties": False}}},
    {"type": "function", "function": {"name": "get_memory", "description": "Retrieve saved user memories.", "parameters": {"type": "object", "properties": {}, "additionalProperties": False}}},
]

FUNCTIONS = {"add_task": tool_add_task, "list_tasks": tool_list_tasks, "add_goal": tool_add_goal, "save_memory": tool_save_memory, "get_memory": tool_get_memory}

SYSTEM_PROMPT = """You are Aura, a helpful personal AI agent.
Be friendly, clear, practical, and concise. Help the user plan, organize, and make progress.
You can use tools to add/list tasks, save goals, and save/retrieve memories.
Only save a memory when the user clearly asks you to remember/save it. Never claim a task, goal, or memory was saved unless the corresponding tool succeeds.
Ask a brief follow-up if essential information is missing. Do not invent dates, completed actions, or personal facts.
When asked to plan, make a realistic prioritized plan and include breaks. The user controls their own data."""

def run_agent(user_message, history=None):
    client = get_client()
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for item in (history or [])[-10:]:
        if item.get("role") in ("user", "assistant") and item.get("content"):
            messages.append({"role": item["role"], "content": item["content"]})
    messages.append({"role": "user", "content": user_message})

    for _ in range(5):
        response = client.chat.completions.create(
            model=MODEL, messages=messages, tools=TOOLS, tool_choice="auto", temperature=0.4
        )
        msg = response.choices[0].message
        if not msg.tool_calls:
            return msg.content or "I'm here. What would you like to work on?"
        messages.append(msg)
        for call in msg.tool_calls:
            name = call.function.name
            try:
                args = json.loads(call.function.arguments or "{}")
                result = FUNCTIONS[name](**args)
            except Exception as exc:
                result = {"success": False, "error": str(exc)}
            messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result, ensure_ascii=False)})
    return "I reached the tool-call limit for this request. Please try a simpler instruction."

def summarize_text(text, style="Clear bullet points"):
    client = get_client()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Summarize only the supplied text. Do not invent facts."},
            {"role": "user", "content": f"Summarize this using the style '{style}':\n\n{text}"}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

def generate_daily_plan(tasks, goals):
    client = get_client()
    task_lines = "\n".join([f"- {t[1]} (priority: {t[2]}, due: {t[3] or 'not set'})" for t in tasks]) or "- No pending tasks"
    goal_lines = "\n".join([f"- {g[1]}: {g[2]}" for g in goals]) or "- No saved goals"
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Create a realistic, prioritized daily plan. Use time blocks but do not assume a start time; label times as suggested. Include breaks and a short end-of-day review."},
            {"role": "user", "content": f"Pending tasks:\n{task_lines}\n\nGoals:\n{goal_lines}\n\nCreate today's plan."}
        ],
        temperature=0.4
    )
    return response.choices[0].message.content
