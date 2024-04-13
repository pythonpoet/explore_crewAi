import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
    SerperDevTool,
    WebsiteSearchTool
)

from prompt import *
from key import *
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1" 

os.environ['OPENAI_MODEL_NAME'] = 'mistralai/mistral-7b-instruct:free'
#os.environ['OPENAI_MODEL_NAME'] = 'mistralai/mixtral-8x22b:free'


# Initialize a tool that the agents will use for research
search_tool = SerperDevTool()
web_rag_tool = WebsiteSearchTool()


# Creating a senior researcher agent
# This agent is tasked with uncovering new information in a specified field
manager = Agent(
    role='Manager',
    goal='Coordinate participants: {users} for the project {project}',
    verbose=True,
    memory=True,
    backstory=(
        "This manager is everybodies dream boss."
        "Very empathetic and very knowlegeable of various managment theories aswell as sociology and psychology"
        "This manager is able to find concensus between the most ego-centric and stubborn individuals"
    ),
    tools=[],  # Assigning research tool to the agent
    allow_delegation=True
)
cook = Agent(
    role='Cook',
    goal='Deliveres a recipe for {menu} ingredients list and cooking instruction',
    verbose=True,
    memory=True,
    backstory=(
        "You are a michelin cook. Your world is the kitchen"
        "You can cook the most extravagant dishes or the most simple one."
        "what you do doesnt really matter since everything becomes magically good if you are in charge of the kitchen"
    ),
    #tools=[search_tool,web_rag_tool],  # Using the same research tool for content creation
    allow_delegation=False
)

# Creating a writer agent
# This agent is responsible for composing narratives based on research findings
researcher = Agent(
    role='Researcher',
    goal='Performs a quick websearch and find a quick answer for the project {project} fast',
    verbose=True,
    memory=True,
    backstory=(
        "With a flair for simplifying complex topics, you always have an easy answer"
    ),
    tools=[search_tool,web_rag_tool],  # Using the same research tool for content creation
    allow_delegation=False
)



# Defining a research task for the senior researcher
idea_task = Task(
    description=(
        "This is the discussion: {discussion} find consensus on {project}"
    ),
    expected_output='One single dish that encorporates all preferences of the group',
    agent=manager,
)

# Defining a writing task for the writer
plan_menu = Task(
    description=(
        "We cook {menu} give instructions on how to cook and list the ingreediences"
    ),
    expected_output='shopping list and instructions on how to cook',
    #tools=[search_tool,web_rag_tool],
    agent=cook,
    async_execution=False,

)
research_task = Task(
    description=(
        "You take the ingreediences list from the cook and search that product on albert heijn and create a shopping list"
    ),
    expected_output='A shopping list formatted as markdown.',
    tools=[search_tool,web_rag_tool],
    agent=researcher,
    async_execution=False,
    output_file='shoppinglist.md'
)
plan_task = Task(
    description=(
        "{users} are going to cook the menu {menu}."
        "While incorperating {list}"
        "Make a task-list that assigns task to everyone of the participants: {users} a task to cook the menu,"
        "pay attention that the tasks are distributed evenly"
    ),
    expected_output='A list containing only the task everyone has to do, formated as markdown',
    agent=manager,
    async_execution=False,
)
# Creating a crew with the researcher and writer agents to collaborate on the project
find_recipe = Crew(
    agents=[manager],
    tasks=[idea_task,],
    process=Process.sequential  # Tasks will be executed one after the other
)

find_ingrediences = Crew(
    agents=[manager, ],
    tasks=[plan_menu],
    process=Process.sequential  
)

assign_tasks = Crew(
    agents=[manager, ],
    tasks=[plan_task],
    process=Process.sequential  
)

recipe = find_recipe.kickoff(inputs={
    'project': 'cook something',
    'users':promt_team,
    'discussion': promt_idea
    })

print(recipe)

shopping_list = find_ingrediences.kickoff(
    inputs={
    'project': 'cook something',
        'users':promt_team,
    'discussion': promt_idea,
    'menu':recipe,
    })

print(shopping_list)

cooking_tasks = assign_tasks.kickoff(
        inputs={
    'project': 'cook something',
        'users':promt_team,
    'discussion': promt_idea,
    'menu':recipe,
    'list': shopping_list
    })

print(cooking_tasks)


""" # Creating a crew with the researcher and writer agents to collaborate on the project
crew = Crew(
    agents=[manager, researcher],
    tasks=[idea_task, research_task, plan_task ],
    process=Process.sequential  # Tasks will be executed one after the other
)

# Kickoff the crew with a specific topic to start the process
result = crew.kickoff(inputs={'project': 'cook something'})
print(result) """