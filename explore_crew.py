import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1" 

os.environ['OPENAI_MODEL_NAME'] = 'mistral'


# Initialize a tool that the agents will use for research
search_tool = SerperDevTool()

# Creating a senior researcher agent
# This agent is tasked with uncovering new information in a specified field
researcher = Agent(
    role='Senior Researcher',
    goal='Uncover groundbreaking technologies in {topic}',
    verbose=True,
    memory=True,
    backstory=(
        "Driven by curiosity, you're at the forefront of "
        "innovation, eager to explore and share knowledge that could change "
        "the world."
    ),
    tools=[search_tool],  # Assigning research tool to the agent
    allow_delegation=True
)

# Creating a writer agent
# This agent is responsible for composing narratives based on research findings
writer = Agent(
    role='Writer',
    goal='Narrate compelling tech stories about {topic}',
    verbose=True,
    memory=True,
    backstory=(
        "With a flair for simplifying complex topics, you craft "
        "engaging narratives that captivate and educate, bringing new "
        "discoveries to light in an accessible manner."
    ),
    tools=[search_tool],  # Using the same research tool for content creation
    allow_delegation=False
)

# Defining a research task for the senior researcher
research_task = Task(
    description=(
        "Identify the next big trend in {topic}. "
        "Focus on identifying pros and cons and the overall narrative. "
        "Your final report should clearly articulate the key points, "
        "its market opportunities, and potential risks."
    ),
    expected_output='A comprehensive 3 paragraphs long report on the latest AI trends.',
    tools=[search_tool],
    agent=researcher,
)

# Defining a writing task for the writer
write_task = Task(
    description=(
        "Compose an insightful article on {topic}. "
        "Focus on the latest trends and how it's impacting the industry. "
        "This article should be easy to understand, engaging, and positive."
    ),
    expected_output='A 4 paragraph article on {topic} advancements formatted as markdown.',
    tools=[search_tool],
    agent=writer,
    async_execution=False,
    output_file='new-blog-post.md'
)

# Creating a crew with the researcher and writer agents to collaborate on the project
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential  # Tasks will be executed one after the other
)

# Kickoff the crew with a specific topic to start the process
result = crew.kickoff(inputs={'topic': 'AI in healthcare'})
print(result)