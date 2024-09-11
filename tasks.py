from crewai import Task
from tools import tool,tool2
from agents import youtube_researcher,blog_researcher,writer


print("research is woorking")

youtube_research_task = Task(
    description="Conduct thorough research on {topic} using credible online sources, synthesizing complex information into clear and concise summaries that will serve as a foundation for high-quality, scholarly articles.",
    expected_output="A detailed research report on [topic] including a summary of key findings, relevant statistics, and references to primary sources as well as links.",
    tools=[tool,tool2],
    agent=youtube_researcher
)

research_task = Task(
    description="Conduct thorough research on {topic} using credible online sources, synthesizing complex information into clear and concise summaries that will serve as a foundation for high-quality, scholarly articles.",
    expected_output="A detailed research report on [topic] including a summary of key findings, relevant statistics, and references to primary sources as well as links.",
    tools=[tool,tool2],
    agent=blog_researcher
)

print("writing start")



writing_task = Task(
    description="Craft high-quality, engaging, and technically accurate content on {topic} that effectively communicates complex concepts to a diverse audience, ensuring clarity, precision, and adherence to industry standards.",
    expected_output="A well-formed article on {topic} including an introduction, key terminologies, steps to perform the specific task mentioned in the topic, relevant image links, and a conclusion formated as a markdown.",
    tools=[tool,tool2],
    agent=writer,
    async_execution=False,
    output_file="output.md"
)