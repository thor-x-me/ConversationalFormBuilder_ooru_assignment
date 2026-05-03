import requests
import traceback
from langchain.tools import tool


BASE_URL = "http://localhost:3001"

@tool
def authenticate(email: str, password: str) -> str:
    """Authenticate with Form.io admin and return the JWT token."""
    url = f"{BASE_URL}/admin/login"
    payload = {"data": {"email": email, "password": password}}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        token = response.headers.get("x-jwt-token")
        if token:
            return token
        else:
            raise Exception("Authentication succeeded but no token returned.")
    else:
        raise Exception(f"Authentication failed: {response.status_code} - {response.text}")


@tool
def create_form(token: str, title: str, name: str, path: str, components: list) -> dict:
    """Create a new form on Form.io via the REST API.

    This function sends a POST request to the Form.io endpoint to register a new form
    with the specified metadata and component structure.

    Args:
        token (str): JWT authentication token for authorizing the API request.
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
        return traceback.format_exc()
    

@tool
def get_form_data(token: str, form_id: str):
    """Retrieve metadata and configuration for a specific form from Form.io.

    Args:
        token (str): JWT authentication token for authorizing the API request.
        form_id (str): Unique identifier of the form.


    Example:
        >>> form_data = get_form_metadata(
        ...     token="eyJhbGc...",
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

    headers = {
        "Content-Type": "application/json",
        "x-jwt-token": token,
    }
    response = requests.get(f"{BASE_URL}/form/{form_id}", headers=headers)

    if response.status_code != 200:
        return traceback.format_exc()

    form_data = response.json()
    return form_data

