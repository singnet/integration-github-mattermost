import json
import sys
from urllib.parse import urljoin

import requests

__version__ = "0.2.0"


def read_message(file_name):
    try:
        with open(file_name, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        log_error(f"Missing {file_name} file, a previous action should populate it.")
    except Exception as e:
        log_error(f"Error reading message: {e}")


def send(webhook, msg):
    try:
        response = requests.post(webhook, json=msg)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        log_error(f"Error sending message: {e}")


def _build_auth_header(token: str):
    """Build the Authorization header with the provided token.

    Args:
        token: Mattermost API token.

    Returns:
        Authorization header.
    """
    return {"Authorization": f"Bearer {token}"}


def get_me(server_url: str, token: str):
    """Get the current user from Mattermost API.

    Args:
        server_url: Mattermost server URL.
        token: Mattermost API token.

    Returns:
        User information.
    """
    headers = _build_auth_header(token)

    try:
        url = urljoin(server_url, "/api/v4/users/me")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise APICallError(f"Error getting current user: GET {url}") from e


def get_user_by_email(server_url: str, token: str, email: str):
    """Get user by email from Mattermost API.

    Args:
        server_url: Mattermost server URL.
        token: Mattermost API token.
        email: User email.

    Returns:
        User information.
    """
    headers = _build_auth_header(token)

    try:
        url = urljoin(server_url, f"/api/v4/users/email/{email}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        error_message = f"Error getting user by email: GET {url}"
        raise APICallError(error_message) from e


def get_user_by_username(server_url: str, token: str, username: str):
    """Get user by username from Mattermost API.

    Args:
        server_url: Mattermost server URL.
        token: Mattermost API token.
        username: User username.

    Returns:
        User information.
    """
    headers = _build_auth_header(token)

    try:
        url = urljoin(server_url, f"/api/v4/users/username/{username}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise APICallError(f"Error getting user by username: GET {url}") from e


def send_message(url: str, token: str, channeld_id: str, message: str):
    """Send a message to a channel.

    Args:
        url: Mattermost server URL.
        token: Mattermost API token.
        channeld_id: Channel ID.
        message: Message to send.

    Returns:
        Message sent.
    """
    headers = _build_auth_header(token)
    data = {"channel_id": channeld_id, "message": message}

    try:
        url = urljoin(url, "/api/v4/posts")
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise APICallError(f"Error sending message: POST {url}") from e


def create_direct_channel(url: str, token: str, from_user_id, to_user_id: str):
    """Create a direct channel between two users.

    Args:
        url: Mattermost server URL.
        token: Mattermost API token.
        user_id: User ID.
        message: Message to send.
        root_id: Root ID.

    Returns:
        Message sent.
    """
    headers = _build_auth_header(token)
    data = [from_user_id, to_user_id]

    try:
        url = urljoin(url, "/api/v4/channels/direct")
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(e.request.body)
        raise APICallError(f"Error sending direct message: POST {url}") from e


class APICallError(Exception):
    """Exception raised for errors in the API call."""


def is_empty(msg):
    return not bool(msg)


def log_error(message):
    print(message, file=sys.stderr)
    sys.exit(1)
