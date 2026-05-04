import requests
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