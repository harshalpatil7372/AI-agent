import os
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
import openai
from PIL import Image
import requests
from io import BytesIO
# from dotenv import load_dotenv
# load_dotenv()
# import os
# from google import genai
# from google.genai import types
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from agents import youtube_researcher, blog_researcher, writer
from tasks import youtube_research_task, research_task, writing_task
from io import BytesIO
from markdown import markdown
from weasyprint import HTML
from crewai_tools import FileReadTool
# from easyocr import Reader

st.set_page_config(page_title="Research & Writing Guru", page_icon="", layout="centered")


async def import_modules():
    global Crew, Process, youtube_researcher, blog_researcher, writer, research_task, writing_task, youtube_research_task
    import importlib
    Crew = importlib.import_module('crewai').Crew
    Process = importlib.import_module('crewai').Process

def run_crew_task(topic, selected_agents, selected_tasks, extracted_text):
    crew = Crew(
        agents=selected_agents,
        tasks=selected_tasks,
        process=Process.sequential,
        knowledge_sources=extracted_text,
        # planning=True,
        # planning_llm=llm
    )
    result = crew.kickoff(inputs={'topic': topic})
    return result

async def process_topic(topic, selected_agents, selected_tasks, extracted_text):
    await import_modules()
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, run_crew_task, topic, selected_agents, selected_tasks, extracted_text)
    return result

def typewriter_effect(text, speed=0.002):
    if not isinstance(text, str):
        text = str(text)
    container = st.empty()
    displayed_text = ""
    for char in text:
        displayed_text += char
        container.markdown(f"{displayed_text}|", unsafe_allow_html=True)
        time.sleep(speed)
    container.markdown(f"{displayed_text}", unsafe_allow_html=True)
    return displayed_text

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_image(prompt, size="1024x1024"):
    """
    Generates an image based on the provided prompt using OpenAI's DALL-E API.
    
    Args:
        prompt (str): The description of the image to generate.
        size (str): The size of the image. Options: "256x256", "512x512", "1024x1024".
    
    Returns:
        PIL.Image.Image: The generated image as a PIL Image object.
    """
    try:
        # Call OpenAI's DALL-E API
        response = openai.images.generate(
            prompt=prompt,
            n=1,  # Generate one image
            size=size
        )
        # Fetch the image URL
        image_url = response["data"][0]["url"]
        # Retrieve and convert the image to a PIL object
        img_response = requests.get(image_url)
        print(img_response)
        image = Image.open(BytesIO(img_response.content))
        return image
    except Exception as e:
        raise RuntimeError(f"Failed to generate image: {e}")

# client = os.getenv("GOOGLE_API_KEY")

# def generate_image(prompt):   //api is not avaliable publically
    # """Generates an image based on the provided prompt."""
    # response = client.models.generate_image(
    #     model='imagen-3.0-generate-002',
    #     prompt=prompt,
    #     config=types.GenerateImageConfig(
    #         negative_prompt='people',
    #         number_of_images=1,
    #         include_rai_reason=True,
    #         output_mime_type='image/jpeg'
    #     )
    # )
    # return response.generated_images[0].image
    # return 0;


def generate_pdf(markdown_text):
    html_content = markdown(markdown_text)
    pdf_buffer = BytesIO()
    HTML(string=html_content).write_pdf(pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer

def main():
    if "previous_inputs" not in st.session_state:
        st.session_state.previous_inputs = []

    st.title("🤖 Research & Writing Automation Guru")
    st.markdown("This tool leverages AI to automate research and writing based on your input topic.")

    default_tasks = ["Writing Task", "Research Task"]
    default_agents = ["Writer", "Blog Researcher"]

    task_agent_mapping = {
        "Research Task": [blog_researcher],
        "Writing Task": [writer],
        "YouTube Research Task": [youtube_researcher]
    }

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

    dynamic_tasks = st.multiselect(
        "Add additional tasks (optional):",
        options=[task for task in available_tasks.keys() if task not in default_tasks],
    )
    all_tasks = default_tasks + dynamic_tasks

    all_agents = set()
    for task in all_tasks:
        all_agents.update(task_agent_mapping.get(task, []))

    additional_agents = st.multiselect(
        "Add additional agents (optional):",
        options=[agent for agent in available_agents.keys() if agent not in default_agents],
    )
    all_agents = list(all_agents | {available_agents[agent] for agent in additional_agents})
    selected_task_objects = [available_tasks[task] for task in all_tasks]


    with st.sidebar.header("Model Selection"):
        model_options = ["DALL-E", "ChatGPT", "Google Imagen", "Custom Model"]
        selected_model = st.selectbox("",model_options, index=0)

   # Sidebar for Image Generation
    st.sidebar.header("Generate Image")
    with st.sidebar.expander("Click to Generate an Image", expanded=False):
        image_prompt = st.text_input("Image Prompt:", key="image_prompt_sidebar")
        size_options = ["256x256", "512x512", "1024x1024"]
        image_size = st.selectbox("Select Image Size:", size_options, index=1)
        generate_button = st.button("Generate", key="generate_image_sidebar")

        if generate_button and image_prompt:
            st.sidebar.info("Generating image... Please wait.")
            try:
                # Generate the image
                image = generate_image(image_prompt, size=image_size)
                st.sidebar.image(image, caption="Generated Image", use_column_width=True)

                # Create a download button
                img_buffer = BytesIO()
                image.save(img_buffer, format="JPEG")
                img_buffer.seek(0)

                st.sidebar.download_button(
                    label="Download Image",
                    data=img_buffer,
                    file_name="generated_image.jpg",
                    mime="image/jpeg"
                )
            except Exception as e:
                st.sidebar.error(f"Error generating image: {e}")


    st.sidebar.header("Previous Topics")
    if st.session_state.previous_inputs:
        for i, topic in enumerate(st.session_state.previous_inputs):
            st.sidebar.write(f"{i + 1}. {topic}")

    uploaded_file = st.file_uploader("Upload a document to extract text (optional):")
    extracted_text = ""

    if uploaded_file is not None:
        file_path = f"/tmp/{uploaded_file.name}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        reader = Reader(['en']) 
        extracted_text = reader.readtext(file_path, detail=0, paragraph=True)
        extracted_text = "\n".join(extracted_text)
        
        st.text_area("Extracted Text", value=extracted_text, height=200)

    with st.form(key="topic_form", clear_on_submit=True):
        st.markdown("### Enter a topic to research and write about:")
        topic = st.text_input("Topic:", key="input_topic")
        submit_button = st.form_submit_button("Generate Content")


    if submit_button:
        if topic:
            st.session_state.previous_inputs.append(topic)
            st.sidebar.write(f"{len(st.session_state.previous_inputs)}. {topic}")

            st.info(f"Generating content for **{topic}**... This may take a moment.")

            with st.spinner('Processing... Please wait...'):
                result = asyncio.run(process_topic(topic, all_agents, selected_task_objects, extracted_text))

            result_text = result.raw or "No output available"

            st.success("Done! Here's the result:")
            final_text = typewriter_effect(result_text)

            pdf_buffer = generate_pdf(final_text)
            st.download_button(
                label="Download as PDF",
                data=pdf_buffer,
                file_name=f"{topic}.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("Please enter a topic before submitting.")

    st.markdown("---")
    st.markdown("© 2024 Impose Agents")

if __name__ == "__main__":
    main()
