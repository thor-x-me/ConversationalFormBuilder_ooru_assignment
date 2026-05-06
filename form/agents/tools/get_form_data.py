import requests
from langchain.tools import tool
from auth.auth import authenticate


BASE_URL = "http://localhost:3001"


@tool
def get_form_data(form_id: str):
    """Retrieve metadata and configuration for a specific form from Form.io.

    Args:
        form_id (str): Unique identifier of the form.


    Example:
        >>> form_data = get_form_metadata(
        ...     form_id="69f6ff82306......"
        ... )
        ... result = dict: {'_id': '69f6ff82306.........',
        ...         'title': 'Contact Form',
        ...         'name': 'contactform',
        ...         'path': 'contactform',
        ...         'type': 'form',
        ...         'display': 'form',
        ...         'tags': [],
        ...         'owner': '69f5f784408..........',
        ...         'components': [{'type': 'textfield', 'key': 'firstName', 'label': 'First Name', 'placeholder': 'Enter your first name', 'input': True, 'validate': {'required': True}}, {'type': 'textfield', 'key': 'lastName', 'label': 'Last Name', 'placeholder': 'Enter your last name', 'input': True, 'validate': {'required': True}}, {'type': 'button', 'key': 'submit', 'label': 'Submit', 'action': 'submit', 'input': True, 'theme': 'primary'}],
        ...         'pdfComponents': [],
        ...         'access': [{'type': 'read_all', 'roles': ['69f5f784408......', '69f5f784408.........', '69f5f784408.......']}],
        ...         'submissionAccess': [],
        ...         'created': '2026-05-03T07:55:46.167Z',
        ...         'modified': '2026-05-03T07:55:46.169Z',
        ...         'machineName': 'contactform'
        ... }

    """
    print("Function get_form_data called ...")
    EMAIL = "admin@example.com"
    PASSWORD = "CHANGEME"
    token = authenticate(EMAIL, PASSWORD)

    headers = {
        "Content-Type": "application/json",
        "x-jwt-token": token,
    }
    response = requests.get(f"{BASE_URL}/form/{form_id}", headers=headers)

    if response.status_code != 200:
        return response.text

    form_data = response.json()
    return form_data
