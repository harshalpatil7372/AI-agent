import streamlit as st
import asyncio
from concurrent.futures import ThreadPoolExecutor

st.set_page_config(page_title="Research & Writing Tool", page_icon="", layout="centered")

# Async function to perform the imports
async def import_modules():
    global Crew, Process, youtube_researcher, blog_researcher, writer, research_task, writing_task, youtube_research_task
    import importlib
    Crew = importlib.import_module('crewai').Crew
    Process = importlib.import_module('crewai').Process
    youtube_researcher = importlib.import_module('agents').youtube_researcher
    blog_researcher = importlib.import_module('agents').blog_researcher
    writer = importlib.import_module('agents').writer
    research_task = importlib.import_module('tasks').research_task
    writing_task = importlib.import_module('tasks').writing_task
    youtube_research_task = importlib.import_module('tasks').youtube_research_task

# Function to run the Crew task
def run_crew_task(topic):
    crew = Crew(
        agents=[youtube_researcher, blog_researcher, writer],
        tasks=[youtube_research_task, research_task, writing_task],
        process=Process.sequential,
    )
    result = crew.kickoff(inputs={'topic': topic})
    return result

# Async function to handle the processing
async def process_topic(topic):
    await import_modules()
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, run_crew_task, topic)
    return result

# Streamlit app layout
def main():
    # Initialize session state to store previous inputs
    if "previous_inputs" not in st.session_state:
        st.session_state.previous_inputs = []

    st.title("🤖 Research & Writing Automation Tool")
    st.markdown("This tool leverages AI to automate research and writing based on your input topic.")

    # Create a sidebar for previous inputs
    st.sidebar.header("Previous Topics")
    if st.session_state.previous_inputs:
        st.sidebar.write(st.session_state.previous_inputs)
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

            st.info(f"Generating content for **{topic}**... This may take a moment.")
            with st.spinner('Processing... Please wait...'):
                result = asyncio.run(process_topic(topic))
            st.success("Done! Here's the result:")
            st.write(result)
        else:
            st.warning("Please enter a topic before submitting.")

    # Footer with additional info
    st.markdown("---")
    st.markdown("© 2024 Impose Agents")

if __name__ == "__main__":
    main()
