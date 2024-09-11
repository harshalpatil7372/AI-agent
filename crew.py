print("execution start at top")


from crewai import Crew,Process
from agents import youtube_researcher,blog_researcher,writer
from tasks import research_task,writing_task,youtube_research_task

print("execution start ")
crew = Crew(
    agents=[youtube_researcher,blog_researcher,writer],
    tasks=[youtube_research_task,research_task,writing_task],
    process=Process.sequential,
)

print("execution end ")


result= crew.kickoff(inputs={'topic':'apple m series chips'})
print(result)


# import streamlit as st
# import asyncio
# from concurrent.futures import ThreadPoolExecutor

# # Define an async function to perform the imports
# async def import_modules():
#     # Import the necessary modules
#     global Crew, Process, youtube_researcher, blog_researcher, writer, research_task, writing_task
#     import importlib
#     Crew = importlib.import_module('crewai').Crew
#     Process = importlib.import_module('crewai').Process
#     youtube_researcher = importlib.import_module('agents').youtube_researcher
#     blog_researcher = importlib.import_module('agents').blog_researcher
#     writer = importlib.import_module('agents').writer
#     research_task = importlib.import_module('tasks').research_task
#     writing_task = importlib.import_module('tasks').writing_task

# # Define the long-running task function
# def run_crew_task(topic):
#     crew = Crew(
#         agents=[youtube_researcher, blog_researcher, writer],
#         tasks=[research_task, writing_task],
#         process=Process.sequential,
#     )
#     result = crew.kickoff(inputs={'topic': topic})
#     return result

# # Create an async function to handle the processing
# async def process_topic(topic):
#     await import_modules()
#     loop = asyncio.get_running_loop()
#     with ThreadPoolExecutor() as pool:
#         result = await loop.run_in_executor(pool, run_crew_task, topic)
#     return result

# # Define the Streamlit app
# def main():
#     st.title("Research and Writing Automation")

#     # Take user input for the topic
#     topic = st.text_input("Enter the topic:")

#     if st.button("Generate"):
#         # Display spinner while processing
#         with st.spinner('Processing... This might take a while, please wait...'):
#             result = asyncio.run(process_topic(topic))

#         # Display the result after processing
#         st.success('Processing complete!')
#         st.write("Result:")
#         st.write(result)

# if __name__ == "__main__":
#     main()
