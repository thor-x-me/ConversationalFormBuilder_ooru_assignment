import requests
from langchain.tools import tool
from auth.auth import authenticate


BASE_URL = "http://localhost:3001"


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
