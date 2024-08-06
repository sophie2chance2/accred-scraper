from selenium import webdriver
from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests
import os

def create_session():
    url = 'https://www.browserbase.com/v1/sessions'
    headers = {'Content-Type': 'application/json', 'x-bb-api-key': os.environ["BROWSERBASE_API_KEY"]}
    response = requests.post(url, json={ "projectId": os.environ["BROWSERBASE_PROJECT_ID"] }, headers=headers)
    return response.json()['id']


class CustomRemoteConnection(RemoteConnection):
    _session_id = None

    def __init__(self, remote_server_addr: str, session_id: str):
        super().__init__(remote_server_addr)
        self._session_id = session_id

    def get_remote_connection_headers(self, parsed_url, keep_alive=False):
        headers = super().get_remote_connection_headers(parsed_url, keep_alive)
        headers.update({'x-bb-api-key': os.environ["BROWSERBASE_API_KEY"]})
        headers.update({'session-id': self._session_id})
        return headers


import html2text
# def run():
from html2text import html2text

url = "https://www.accsc.org/Directory/index.aspx"

session_id = create_session()
custom_conn = CustomRemoteConnection('http://connect.browserbase.com/webdriver', session_id)
options = webdriver.ChromeOptions()
options.debugger_address = "localhost:9223"
driver = webdriver.Remote(custom_conn, options=options)
driver.get(url)
page = driver.page_source
get_title = driver.title
print(get_title)
# content = html2text(page.content())
driver.switch_to.frame("frmDirSearch")
search_box = driver.find_element(by="id", value="txtSchoolSearch")
search_box.send_keys("Concorde Career College")
accept_button = driver.find_element(by="id", value="btnSearch")
accept_button.click()

result_table = driver.find_element(by='id', value='grdResult')
page_html = result_table.get_attribute('innerHTML')
html2text(page_html)
print(page_html)

# accept_button = driver.find_element(by="id", value="btnSearch")
# Make sure to quit the driver so your session is ended!
driver.quit()

# run()











from crewai import Crew, Task, Agent
from dotenv import load_dotenv
import sys
load_dotenv()

accreditor_agent = Agent(
    role="Accreditor Search",
    goal="Search accreditors",
    backstory="I am an agent that can search for schools in an accreditor database.",
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

crew = Crew(
    agents=[accreditor_agent],
    tasks=[search_task],
    # let's cap the number of OpenAI requests as the Agents
    #   may have to do multiple costly calls with large context
    max_rpm=100,
)

result = crew.kickoff(
    inputs={
        "request": "Paul Mitchell Schools",
    }
)
print(result)
