import requests
import traceback
from langchain.tools import tool


BASE_URL = "http://localhost:3001"

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
            return "Authentication succeeded but no token returned."
    else:
        return f"Authentication failed: {response.status_code} - {response.text}"


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

@tool
def update_form(form_id: str, old_form: dict, modified_component: list[dict]):
    """Update a form's components via API and return the result.
    
    Args:
        form_id: The unique identifier of the form to update.
        old_form: The original form dictionary (will be mutated).
        modified_component: The list new component(s) to replace form["components"].
    
    Returns:
        dict: Updated form response if successful.
        str: Error message if the update request fails.
    """

    old_form["components"] = modified_component
    EMAIL = "admin@example.com"
    PASSWORD = "CHANGEME"
    token = authenticate(EMAIL, PASSWORD)

    headers = {
        "Content-Type": "application/json",
        "x-jwt-token": token,
    }
    update_response = requests.put(
        f"{BASE_URL}/form/{form_id}",
        json=old_form,
        headers=headers,
    )

    if update_response.status_code == 200:
        updated = update_response.json()
        return updated
    else:
        return f"Update failed: {update_response.status_code} - {update_response.text}"

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

@tool
def get_created_forms():
    """
    This endpoint lists all forms within the project.
    """
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