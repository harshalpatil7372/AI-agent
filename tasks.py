from crewai import Task
from tools import tool,tool2,yt_tool
from agents import youtube_researcher,blog_researcher,writer
from langchain_community.tools import YouTubeSearchTool


print("research is woorking")


youtube_research_task = Task(
    description="Conduct thorough research on {topic} using credible online sources, synthesizing complex information into clear and concise summaries that will serve as a foundation for high-quality, scholarly articles.",
    expected_output="A detailed research report on {topic} including a summary of key findings, relevant statistics, and references to primary sources as well as links.",
    tools=[tool,yt_tool],
    max_iter=3,
    agent=youtube_researcher
)

research_task = Task(
    description="Conduct thorough research on {topic} using credible online sources, synthesizing complex information into clear and concise summaries that will serve as a foundation for high-quality, scholarly articles.",
    expected_output="A detailed research report on {topic} including a summary of key findings, relevant statistics, and references to primary sources as well as links.",
    tools=[tool,yt_tool],
    agent=blog_researcher
)

print("writing start")



writing_task = Task(
    description=(
        "Craft high-quality, engaging, and technically accurate content on {topic} that effectively communicates complex concepts "
        "to a diverse audience. The article should include relatable examples, use a conversational tone, and be indistinguishable "
        "from human-written content. Images relevant to the topic should be incorporated with proper Markdown syntax for visual engagement."
    ),
    expected_output=(
        "A well-structured article on {topic} formatted as Markdown. The article must include: "
        "Eye catching head line which should not include word like research report. "
        "- Introduction: A brief overview of the topic. "
        "- Key Terminologies: Clear definitions of important terms. "
        "- Main Content: Steps, guides, or detailed explanations of the topic. "
        "- Images: Relevant images inserted with proper Markdown links and alt text. "
        "- Conclusion: A summary or actionable takeaways. "
        "The tone should be natural, engaging, and easy to understand."
    ),
    tools=[tool, yt_tool],
    agent=writer,  # Assign the updated writer agent
    async_execution=False,  # Set to True if task execution should not block
    output_file="output.md"  # Output will be saved in a Markdown file
)
