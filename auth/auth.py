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
