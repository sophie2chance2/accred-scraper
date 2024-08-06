import requests
import os
from dotenv import load_dotenv
load_dotenv()

def create_session():
    url = 'https://www.browserbase.com/v1/sessions'
    headers = {'Content-Type': 'application/json', 'x-bb-api-key': os.environ["BROWSERBASE_API_KEY"]}
    response = requests.post(url, json={ "projectId": os.environ["BROWSERBASE_PROJECT_ID"] }, headers=headers, timeout=10)
    return response.json()['id']


def live_debug(session_id):
    url = f"https://www.browserbase.com/v1/sessions/{session_id}/debug"
    headers = {"X-BB-API-Key": os.environ["BROWSERBASE_API_KEY"]}
    response = requests.request("GET", url, headers=headers, timeout=10)
    return response.json()['debuggerFullscreenUrl']