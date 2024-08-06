
from selenium import webdriver
from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.webdriver.support.ui import Select
import requests
import os
from time import sleep
from html2text import html2text
from dotenv import load_dotenv
from crewai_tools import tool
from typing import Optional
load_dotenv()

def create_session():
    url = 'https://www.browserbase.com/v1/sessions'
    headers = {'Content-Type': 'application/json', 'x-bb-api-key': os.environ["BROWSERBASE_API_KEY"]}
    response = requests.post(url, json={ "projectId": os.environ["BROWSERBASE_PROJECT_ID"] }, headers=headers, timeout=10)
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

@tool("accred_accsc")
def accred_accsc(school_name: str, state: Optional[str] = '') -> str: 
    """Input search parameters to find a school(s) in the ACCSC database. 
    school_name: name of the school to search for
    state (optional): full name of the state

    Returns the search results."""
    url = "https://www.accsc.org/Directory/index.aspx"

    session_id = create_session()
    custom_conn = CustomRemoteConnection('http://connect.browserbase.com/webdriver', session_id)
    options = webdriver.ChromeOptions()
    options.debugger_address = "localhost:9223"
    driver = webdriver.Remote(custom_conn, options=options)
    driver.get(url)
    driver.switch_to.frame("frmDirSearch")

    print("Waiting for page to load...")
    sleep(1)

    search_box = driver.find_element(by="id", value="txtSchoolSearch")
    search_box.send_keys(school_name)

    print(f"Searching for {school_name}...")
    # sleep(2)

    if state != '':
        states_list = driver.find_element(by="id", value="lstLocation")
        select = Select(states_list)
        select.select_by_visible_text(state.upper())

        print(f"Searching for {state}...")
        # sleep(2)

    accept_button = driver.find_element(by="id", value="btnSearch")
    accept_button.click()

    print("Getting search results...")
    sleep(2)

    try:
        result_table = driver.find_element(by='id', value='grdResult')
        page_html = result_table.get_attribute('innerHTML')
        search_results = html2text(page_html)
    except:
        search_results = "Not accredited by ACCSC."
    driver.quit()

    return search_results