import requests
from langchain.tools import tool
from form_io import authenticate


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

@tool
def update_form(form_id: str, modified_form: dict):
    """Update a form's components via API and return the result.
    
    Args:
        form_id: The unique identifier of the form to update.
        modified_form: The  new form with same _id as old form.
    
    Returns:
        dict: Updated form response if successful.
        str: Error message if the update request fails.
    """
    print("Function update_form called ...")
    EMAIL = "admin@example.com"
    PASSWORD = "CHANGEME"
    token = authenticate(EMAIL, PASSWORD)

    headers = {
        "Content-Type": "application/json",
        "x-jwt-token": token,
    }
    update_response = requests.put(
        f"{BASE_URL}/form/{form_id}",
        json=modified_form,
        headers=headers,
    )

    if update_response.status_code == 200:
        updated_form = update_response.json()
        return updated_form
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