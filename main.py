# import sys
# from crewai_tools import tool
from crewai import Crew, Task, Agent
from dotenv import load_dotenv
load_dotenv()

from accreditors import accred_accsc, accred_abhes
from browserbase import create_session, live_debug

##################################### CREW #######################################
################################ Accreditor Search ###############################
accred_search_agent = Agent(
    role="Accreditor Search",
    goal="Get as many key insights about the schools as possible from the various accreditors.",
    backstory="I am an agent that can search for schools in an accreditor databases. I get key insights about the schools that are helpful for the sales team. First I will search for the schools in the ACCSC database and then in the ABHES database.",
    tools=[accred_accsc, accred_abhes],
    allow_delegation=False,
)

accred_search_example = """
School Name: ABC School - New York
Location: New York, NY
Website: www.abcschool.com
Programs: Nursing, Business
Accreditation: ACCSC, ABHES
Next Accreditation: 12/5/2027
Key Contacts: 
    Name: John Doe
    Title: President
    Phone: 123-456-7890
    Email: jdoe@abc.com
School Name: ABC School - San Diego
Location: San Diego, CA
Website: www.abcschool.com
Programs: Dentist, Beauty
Accreditation: ACCSC
Next Accreditation: 11/10/2025
Key Contacts: 
    Name: Jane Doe
    Title: President
    Phone: 123-456-7890
    Email: jdoe@abc.com
"""

accred_search_task = Task(
    description=(
        "Search schools to find their key insights based on the request: {request}. Use this Session ID: {session_id}"
    ),
    expected_output=accred_search_example,
    agent=accred_search_agent,
    # context=[search_input_task]
)
################################## Call Crew #####################################
crew = Crew(
    agents=[accred_search_agent], 
    tasks=[accred_search_task],
    max_rpm=100,
)

def call_crew(request: str):
    session_id = create_session()
    debug_url = live_debug(session_id)
    print(f"Debug URL: {debug_url}")

    result = crew.kickoff(
        inputs={
            "request": request,
            "session_id": session_id
        }
    )
    
    post_session_url = f"https://www.browserbase.com/sessions/{session_id}"
    print(f"Post Session URL: {post_session_url}")

    return result

output = call_crew("Tell me about the school Genesis")
print(output)








































################################# AGENT GRAVEYARD ##################################

# search_params_agent = Agent(
#     role="HTML Search Parameter Finder",
#     goal="Return a dictionary of search parameters with their function as the key and a tuple with the id and selenium action type",
#     backstory="I am an agent that can find search parameters for a given HTML page.",
#     tools=[find_params],
#     allow_delegation=False,
# )

# output_params_example = """
# School Name: txtSchoolSearch, send_keys
# State: lstLocation, select_by_visible_text
# Search Button: btnSearch, click
# """
# # {'school_name': ('txtSchoolSearch', 'send_keys'), 'state': ('lstLocation', 'select_by_visible_text'), 'search_button': ('btnSearch', 'click')}

# params_task = Task(
#     description=(
#         "Find search parameters for the given URL: {url}"
#     ),
#     expected_output=output_params_example,
#     agent=search_params_agent,
# )

############################### Search Input Agent ###############################

# search_input_agent = Agent(
#     role="Accreditor Search",
#     goal="Get the search request for the accreditor search agent. Should only return the searchable items.",
#     backstory="I am an agent that simplifies the search request for the accreditor search agent.",
#     allow_delegation=False,
# )

# search_input_example = """Search for ABC"""

# search_input_task = Task(
#     description=(
#         "Find only the searchable items in the request: {request}."
#     ),
#     expected_output=search_input_example,
#     agent=search_input_agent,
# )

################################ Accreditor Search ###############################
# question_response_agent = Agent(
#     role="Question Answering",
#     goal="Answer the question based on the context.",
#     backstory="I am an agent that can answer questions based on the context.",
#     allow_delegation=False,
# )

# question_response_example = """
# The key contacts for ABC School - New York are:
#     Name: John Doe
#     Title: President
#     Phone: 123-456-7890
#     Email: jdoe@abc.com
# """

# question_response_task = Task(
#     description=(
#         "Answer the user's question based on the context. The question is: {request}"
#     ),
#     expected_output=question_response_example,
#     agent=question_response_agent,
#     context=[accred_search_task]
# )