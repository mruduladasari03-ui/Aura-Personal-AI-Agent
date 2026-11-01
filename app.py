import streamlit as st
from dotenv import load_dotenv
from database import init_db, add_task, list_tasks, update_task_status, delete_task, add_goal, list_goals, add_memory, list_memories, add_note, list_notes
from agent import run_agent, summarize_text, generate_daily_plan

load_dotenv()
st.set_page_config(page_title="Aura | Personal AI Agent", page_icon="✨", layout="wide")
init_db()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');

:root {
  --ink: #292344;
  --muted: #817b99;
  --purple: #7663d8;
  --purple-dark: #5c49bd;
  --lavender: #f0edff;
  --line: #e9e4f7;
}
html, body, [class*="css"] {
  font-family: 'DM Sans', sans-serif;
}
.stApp {
  background: linear-gradient(135deg, #fbfaff 0%, #f7f5ff 48%, #fdfbff 100%);
  color: var(--ink);
}
.block-container {
  padding-top: 2rem;
  padding-bottom: 3rem;
  max-width: 1240px;
}
[data-testid="stSidebar"] {
  background: #ffffff;
  border-right: 1px solid var(--line);
}
[data-testid="stSidebar"] * { color: var(--ink); }
[data-testid="stSidebar"] [data-testid="stRadio"] label {
  padding: .45rem .6rem;
  border-radius: 10px;
}
.hero {
  padding: 1.8rem 2rem;
  border: 1px solid #e8e1ff;
  border-radius: 24px;
  background: linear-gradient(115deg, #eeeaff 0%, #faf8ff 55%, #f2efff 100%);
  box-shadow: 0 12px 35px rgba(91, 72, 160, .07);
}
.hero h1 {
  margin: 0;
  color: #30264f;
  font-family: 'Manrope', sans-serif;
  font-size: 2.45rem;
  font-weight: 800;
  letter-spacing: -1.3px;
}
.hero p { color: #756c91; margin: .35rem 0 0 0; font-size: 1.02rem; }
h1, h2, h3 { color: #30264f; font-family: 'Manrope', sans-serif; }
p, label, li { color: #48415f; }
.small-muted { color: #918aa8; font-size: .88rem; }
div[data-testid="stChatMessage"] {
  background: #ffffff;
  border: 1px solid #ece7f7;
  border-radius: 18px;
  padding: 1rem;
  box-shadow: 0 5px 18px rgba(55, 42, 100, .035);
}
div[data-testid="stChatInput"] {
  border: 1px solid #ded6f4;
  border-radius: 18px;
  background: #fff;
}
.stButton > button, .stFormSubmitButton > button {
  background: linear-gradient(135deg, #806de2, #6955c9);
  color: white;
  border: 0;
  border-radius: 12px;
  padding: .55rem 1rem;
  font-weight: 600;
  box-shadow: 0 5px 14px rgba(105, 85, 201, .16);
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
  color: white;
  border: 0;
  background: linear-gradient(135deg, #705dd2, #5b48b7);
}
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea,
div[data-testid="stSelectbox"] > div,
div[data-testid="stDateInput"] input {
  background: #fff;
  border-color: #e3ddf1;
  border-radius: 11px;
}
div[data-testid="stExpander"] {
  background: #fff;
  border: 1px solid #e9e4f5;
  border-radius: 14px;
}
hr { border-color: #e9e4f5; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("✨ Aura")
    st.caption("Your personal AI workspace")
    page = st.radio("Workspace", ["AI Chat", "Tasks", "Daily Planner", "Goals", "Memory & Notes", "Summarizer"])
    st.divider()
    st.caption("Your data is stored locally in SQLite.")
    if st.button("Clear chat history", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown('<div class="hero"><h1>✦ Aura</h1><p>Your calm space to think clearly, plan your day and make progress.</p></div>', unsafe_allow_html=True)
st.write("")

if "messages" not in st.session_state:
    st.session_state.messages = []

if page == "AI Chat":
    st.subheader("Talk to Aura")
    st.caption("Ask questions, manage tasks, save useful memories, or plan your day.")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    prompt = st.chat_input("What would you like me to do?")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Aura is thinking..."):
                try:
                    answer = run_agent(prompt, st.session_state.messages[:-1])
                except Exception as exc:
                    answer = f"**Something went wrong:** {exc}\n\nCheck that your `OPENAI_API_KEY` is set in the `.env` file."
                st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

elif page == "Tasks":
    st.subheader("Task Manager")
    with st.form("new_task", clear_on_submit=True):
        title = st.text_input("Task")
        priority = st.selectbox("Priority", ["Medium", "High", "Low"])
        due_date = st.date_input("Due date", value=None)
        submitted = st.form_submit_button("Add task")
        if submitted and title.strip():
            add_task(title.strip(), priority, str(due_date) if due_date else "")
            st.success("Task added.")
    tasks = list_tasks()
    if not tasks:
        st.info("No tasks yet. Add your first task above.")
    for task in tasks:
        tid, title, priority, due, status, created = task
        c1, c2, c3 = st.columns([6, 2, 1])
        with c1:
            label = f"~~{title}~~" if status == "Done" else title
            st.markdown(f"**{label}**  \n<small>Priority: {priority} · Due: {due or 'Not set'} · {status}</small>", unsafe_allow_html=True)
        with c2:
            if status != "Done" and st.button("Complete", key=f"done{tid}"):
                update_task_status(tid, "Done"); st.rerun()
            elif status == "Done" and st.button("Reopen", key=f"reopen{tid}"):
                update_task_status(tid, "Pending"); st.rerun()
        with c3:
            if st.button("🗑️", key=f"del{tid}"):
                delete_task(tid); st.rerun()
        st.divider()

elif page == "Daily Planner":
    st.subheader("Daily Planner")
    tasks = list_tasks(status="Pending")
    if st.button("Generate my plan", type="primary"):
        with st.spinner("Building a realistic plan..."):
            try:
                plan = generate_daily_plan(tasks, list_goals())
                st.session_state.daily_plan = plan
            except Exception as exc:
                st.error(f"Could not generate plan: {exc}")
    if st.session_state.get("daily_plan"):
        st.markdown(st.session_state.daily_plan)
    if not tasks:
        st.info("Add pending tasks in Task Manager first.")

elif page == "Goals":
    st.subheader("Goal Tracker")
    with st.form("new_goal", clear_on_submit=True):
        goal = st.text_input("What do you want to achieve?")
        description = st.text_area("Why does this goal matter? (optional)")
        submitted = st.form_submit_button("Add goal")
        if submitted and goal.strip():
            add_goal(goal.strip(), description.strip())
            st.success("Goal saved.")
    for gid, title, description, created in list_goals():
        with st.container(border=True):
            st.markdown(f"**{title}**")
            if description: st.write(description)
            st.caption(f"Created: {created}")

elif page == "Memory & Notes":
    st.subheader("Memory & Notes")
    st.markdown("Save stable preferences or useful facts Aura can use in future chats.")
    with st.form("memory_form", clear_on_submit=True):
        memory = st.text_input("Memory")
        if st.form_submit_button("Save memory") and memory.strip():
            add_memory(memory.strip()); st.success("Memory saved.")
    for mid, content, created in list_memories():
        st.markdown(f"- {content}  \n  <small>{created}</small>", unsafe_allow_html=True)
    st.divider()
    st.markdown("**Quick notes**")
    with st.form("note_form", clear_on_submit=True):
        note_title = st.text_input("Note title")
        note_body = st.text_area("Note")
        if st.form_submit_button("Save note") and note_body.strip():
            add_note(note_title.strip() or "Untitled", note_body.strip()); st.success("Note saved.")
    for nid, title, body, created in list_notes():
        with st.expander(title):
            st.write(body)
            st.caption(created)

elif page == "Summarizer":
    st.subheader("AI Summarizer")
    text = st.text_area("Paste text to summarize", height=250, placeholder="Paste an article, class notes, meeting notes...")
    style = st.selectbox("Summary style", ["Clear bullet points", "Short paragraph", "Study notes", "Action items"])
    if st.button("Summarize", type="primary", disabled=not text.strip()):
        with st.spinner("Summarizing..."):
            try:
                st.markdown(summarize_text(text, style))
            except Exception as exc:
                st.error(f"Could not summarize: {exc}")

st.markdown("---")
st.markdown('<p class="small-muted">AURA · YOUR PERSONAL AI SPACE · Built with Python, Streamlit, OpenAI and SQLite</p>', unsafe_allow_html=True)
