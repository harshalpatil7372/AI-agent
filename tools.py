from crewai_tools import SerperDevTool,YoutubeVideoSearchTool  #DallETool  #ScrapeWebsiteTool
from langchain_community.tools import YouTubeSearchTool
from dotenv import load_dotenv
load_dotenv()
import os

os.environ['SERPER_API_KEY']=os.getenv('SERPER_API_KEY')

yt_tool = YouTubeSearchTool()

tool = SerperDevTool()

# img_genertation_tool = dalle_tool = DallETool(model="dall-e-3",
#                        size="1024x1024",
#                        quality="standard",
#                        n=1)

# scrap_tool = ScrapeWebsiteTool()
# tool = ScrapeWebsiteTool(website_url='https://unsplash.com/')

tool2 = YoutubeVideoSearchTool(
    config=dict(
        llm=dict(
            provider="ollama", # or google, openai, anthropic, llama2, ...
            config=dict(
                model="llama2",
                temperature=0.5,
                top_p=1,
                stream=True,
            ),
        ),
        embedder=dict(
            provider="google", # or openai, ollama, ...
            config=dict(
                model="models/embedding-001",
                task_type="retrieval_document",
                # title="Embeddings",
            ),
        ),
    )
)