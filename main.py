# from browserbase import browserbase
from accreditors import accred_accsc
import sys
from crewai import Crew, Task, Agent
from dotenv import load_dotenv
load_dotenv()
from crewai_tools import tool

accreditor_agent = Agent(
    role="Accreditor Search",
    goal="Search accreditors",
    backstory="I am an agent that can search for schools in an accreditor database.",
    tools=[accred_accsc],
    allow_delegation=False,
)

output_search_example = """
Here are some Key Insights about Concorde Career College:
- There are 16 campuses in the United States.
- The college offers programs in healthcare, dental, and nursing.
- The college is accredited by the Accrediting Commission of Career Schools and Colleges (ACCSC).
- Their next accreditation review is in 2026.
- Their website is [here](https://www.concorde.edu/).
"""

search_task = Task(
    description=(
        "Search schools according to criteria {request}."
    ),
    expected_output=output_search_example,
    agent=accreditor_agent,
)

# Tasks and Agents definitions...

crew = Crew(
    agents=[accreditor_agent],
    tasks=[search_task],
    # let's cap the number of OpenAI requests as the Agents
    #   may have to do multiple costly calls with large context
    max_rpm=100,
)

def call_crew(request: str):
    result = crew.kickoff(
        inputs={
            "request": request,
        }
    )
    return result

# print(result)
