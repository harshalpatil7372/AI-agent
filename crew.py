import streamlit as st
import asyncio
from concurrent.futures import ThreadPoolExecutor
from agents import youtube_researcher,blog_researcher,writer
from tasks import youtube_research_task,research_task,writing_task

st.set_page_config(page_title="Research & Writing Tool", page_icon="", layout="centered")

# Async function to perform the imports
async def import_modules():
    global Crew, Process, youtube_researcher, blog_researcher, writer, research_task, writing_task, youtube_research_task
    import importlib
    Crew = importlib.import_module('crewai').Crew
    Process = importlib.import_module('crewai').Process
  

# Function to run the Crew task
def run_crew_task(topic, selected_agents, selected_tasks):
    crew = Crew(
        agents=selected_agents,
        tasks=selected_tasks,
        process=Process.sequential,
    )
    result = crew.kickoff(inputs={'topic': topic})
    return result

# Async function to handle the processing
async def process_topic(topic, selected_agents, selected_tasks):
    await import_modules()
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, run_crew_task, topic, selected_agents, selected_tasks)
    return result

# Streamlit app layout
def main():
    # Initialize session state to store previous inputs
    if "previous_inputs" not in st.session_state:
        st.session_state.previous_inputs = []

    st.title("🤖 Research & Writing Automation Tool")
    st.markdown("This tool leverages AI to automate research and writing based on your input topic.")

    # Available agents and tasks
    available_agents = {
        "YouTube Researcher": youtube_researcher,
        "Blog Researcher": blog_researcher,
        "Writer": writer
    }

    available_tasks = {
        "Research Task": research_task,
        "Writing Task": writing_task,
        "YouTube Research Task": youtube_research_task
    }

    # Sidebar multiselect for agents and tasks
    selected_agents = st.multiselect(
        "Select agents to include:", 
        options=list(available_agents.keys()), 
        default=["Writer"]
    )

    if "Writer" not in selected_agents:
        selected_agents.append("Writer")

    selected_tasks = st.multiselect(
        "Select tasks to include:", 
        options=list(available_tasks.keys()), 
        default=["Writing Task","Research Task"]
    )

    # Map selected agent and task names to actual objects
    selected_agent_objects = [available_agents[agent] for agent in selected_agents]
    selected_task_objects = [available_tasks[task] for task in selected_tasks]

    # Display previous topics
    st.sidebar.header("Previous Topics")
    if st.session_state.previous_inputs:
        for i, topic in enumerate(st.session_state.previous_inputs):
            st.sidebar.write(f"{i + 1}. {topic}")
    else:
        st.sidebar.write("No previous topics in this session yet.")

    # Place the input in the middle of the screen
    with st.form(key="topic_form", clear_on_submit=True):
        st.markdown("### Enter a topic to research and write about:")
        topic = st.text_input("Topic:", key="input_topic")
        submit_button = st.form_submit_button("Generate Content")

    if submit_button:
        if topic:
            # Add input to session state
            st.session_state.previous_inputs.append(topic)

            # Display the topic immediately in the sidebar
            st.sidebar.write(f"{len(st.session_state.previous_inputs)}. {topic}")

            st.info(f"Generating content for **{topic}**... This may take a moment.")
            with st.spinner('Processing... Please wait...'):
                result = asyncio.run(process_topic(topic, selected_agent_objects, selected_task_objects))
            st.success("Done! Here's the result:")
            st.markdown(result, unsafe_allow_html=True)
        else:
            st.warning("Please enter a topic before submitting.")

    # Footer with additional info
    st.markdown("---")
    st.markdown("© 2024 Impose Agents")

if __name__ == "__main__":
    main()
