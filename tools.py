from crewai_tools import SerperDevTool,YoutubeVideoSearchTool
from dotenv import load_dotenv
load_dotenv()
import os

os.environ['SERPER_API_KEY']=os.getenv('SERPER_API_KEY')

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

tool = SerperDevTool()
