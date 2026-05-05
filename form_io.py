import requests
import json
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
            raise ValueError("Authentication succeeded but no token returned.")
    else:
        raise RuntimeError(f"Authentication failed: {response.status_code} - {response.text}")


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
        raise RuntimeError(f"Failed to fetch forms: {response.status_code} {response.text}")

    form_list = response.json()
    return form_list


def get_form_data(form_id: str):
    """Retrieve metadata and configuration for a specific form from Form.io.

    Args:
        form_id (str): Unique identifier of the form.

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
        raise response.text

    form_data = response.json()
    return form_data

def get_versioned_form_data():
    with open("form_data.json") as f:
        data = json.load(f)
    return data

def add_versioned_form(form_id, version, new_form):

    try:
        with open("form_data.json") as f:
            data = json.load(f)
    except json.decoder.JSONDecodeError as e:
        data = []

    new_form_body = {form_id: {version: new_form}}
    data.append(new_form_body)

    with open("form_data.json", "w") as f:
        json.dump(data, f, indent=4)
    return new_form_body

def update_versioned_form(form_id, version, updated_form):
    with open("form_data.json") as f:
        data = json.load(f)

    index = next((i for i, item in enumerate(data) if item["id"] == form_id), None)
    if index is not None:
        data[index][version] = updated_form

        with open("form_data.json", "w") as f:
            json.dump(data, f, indent=4)
        return True
    else:
        return False

def get_versioned_form(form_id, version):
    with open("form_data.json") as f:
        data = json.load(f)

    form = next((item for item in data if item["id"] == form_id), None)

    if form:
        versioned_form = form.get(version)
    else:
        return {}
    return versioned_form

def update_form(form_id: str, modified_form: dict):
    """
    Update a form's  via API and return the result.
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
        updated = update_response.json()
        return updated
    else:
        raise RuntimeError(f"Update failed: {update_response.status_code} - {update_response.text}")
