import requests
from langchain.tools import tool
from auth.auth import authenticate


BASE_URL = "http://localhost:3001"

@tool
def create_form(title: str, name: str, path: str, components: list) -> dict:
    """Create a new form on Form.io via the REST API.

    Args:
        title (str): Human-readable title of the form (displayed to users).
        name (str): Machine-readable identifier for the form (used in URLs and API calls).
        path (str): URL-friendly path/slug for accessing the form (e.g., 'my-form').
        components (list): List of dictionaries defining form fields and layout components
                          following the Form.io component schema.

    Example:
        >>> components = [
        {"type": "textfield", "key": "firstName", "label": "First Name", "placeholder": "Enter your first name", "input": True, "validate": {"required": True},},
        {"type": "textfield", "key": "lastName", "label": "Last Name", "placeholder": "Enter your last name", "input": True, "validate": {"required": True},},
        {"type": "email", "key": "email", "label": "Email Address", "placeholder": "Enter your email", "input": True, "validate": {"required": True},},
        ... ]
        >>> result = {
        ...     '_id': "69f6ff823066........",
        ...     'title':"Contact Form",
        ...     'name':"contactForm",
        ...     'path':"contact",
        ...     'type':"form",
        ...     'display':"form",
        ...     'tags':[],
        ...     'owner':"69f5f784408........",
        ...     'components':[{'type': 'textfield', 'key': 'firstName', 'label': 'First Name', 'placeholder': 'Enter your first name', 'input': True, 'validate': {'required': True}}, {'type': 'textfield', 'key': 'lastName', 'label': 'Last Name', 'placeholder': 'Enter your last name', 'input': True, 'validate': {'required': True}}, {'type': 'email', 'key': 'email', 'label': 'Email Address', 'placeholder': 'Enter your email', 'input': True, 'validate': {'required': True}},],
        ...     'pdfComponents':[],
        ...     'access':[{'type': 'read_all', 'roles': ['69f5f784408........', '69f5f784408.........', '69f5f784408..........']}],
        ...     'submissionAccess': [],
        ...     'created': '2026-05-03T07:55:46.167Z',
        ...     'modified': '2026-05-03T07:55:46.169Z',
        ...     'machineName': 'contactform'
        ... }
    """
    EMAIL = "admin@example.com"
    PASSWORD = "CHANGEME"
    token = authenticate(EMAIL, PASSWORD)
    url = f"{BASE_URL}/form"
    headers = {
        "Content-Type": "application/json",
        "x-jwt-token": token,
    }

    form_definition = {
        "title": title,
        "name": name,
        "path": path,
        "type": "form",
        "display": "form",
        "components": components,
    }

    response = requests.post(url, json=form_definition, headers=headers)

    if response.status_code == 201:
        form = response.json()
        return form
    else:
        return response.text