import requests
from langchain.tools import tool
from auth.auth import authenticate


BASE_URL = "http://localhost:3001"


@tool
def get_created_forms():
    """
    This endpoint lists all forms within the project.
    """
    print("Function get_created_forms called ...")
    EMAIL = "admin@example.com"
    PASSWORD = "CHANGEME"
    token = authenticate(EMAIL, PASSWORD)
    url = f"{BASE_URL}/form"
    headers = {
        "Content-Type": "application/json",
        "x-jwt-token": token,
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return response.text

    form_list = response.json()
    return form_list