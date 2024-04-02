import io
import json
from unittest.mock import mock_open, patch

import pytest
import requests

from mattermost import (
    APICallError,
    create_direct_channel,
    get_me,
    get_user_by_email,
    get_user_by_username,
    is_empty,
    log_error,
    read_message,
    send,
    send_message,
)


def test_read_message_file_not_found(capsys):
    error_message = (
        "Missing nonexistent_file.json file, a previous action should populate it."
    )

    with patch("builtins.open", side_effect=FileNotFoundError):
        try:
            read_message("nonexistent_file.json") is None
        except SystemExit as e:
            captured = capsys.readouterr()
            assert error_message in captured.err
            assert e.code == 1
        else:
            assert False, "log_error did not raise a SystemExit exception"


def test_read_message_invalid_json(capsys):
    error_message = "Error reading message"
    with patch("builtins.open", return_value=io.StringIO("invalid JSON")):
        try:
            read_message("invalid_json.json") is None
        except SystemExit as e:
            captured = capsys.readouterr()
            assert error_message in captured.err
            assert e.code == 1
        else:
            assert False, "log_error did not raise a SystemExit exception"


def test_read_message_success():
    json_content = {"text": "hello world"}

    with patch("builtins.open", new=mock_open(read_data=json.dumps(json_content))):
        result = read_message("fake_file.json")

    assert result == json_content


def test_send_successful_post(monkeypatch, capsys):
    def mock_post(*args, **kwargs):
        class MockResponse:
            status_code = 200

            def raise_for_status(self):
                pass

        return MockResponse()

    monkeypatch.setattr(requests, "post", mock_post)
    send("fake_webhook", {"text": "test_message"})
    captured = capsys.readouterr()
    assert "Error sending message" not in captured.err


def test_send_failed_post(monkeypatch, capsys):
    def mock_post(*args, **kwargs):
        raise requests.exceptions.RequestException()

    monkeypatch.setattr(requests, "post", mock_post)
    error_message = "Error sending message"

    try:
        send("fake_webhook", {"text": "test_message"})
    except SystemExit as e:
        captured = capsys.readouterr()
        assert error_message in captured.err
        assert e.code == 1
    else:
        assert False, "log_error did not raise a SystemExit exception"


def test_is_empty():
    assert is_empty(None) is True
    assert is_empty("") is True
    assert is_empty({"text": "test"}) is False


def test_log_error(capsys):
    error_message = "Test error message"
    try:
        log_error(error_message)
    except SystemExit as e:
        captured = capsys.readouterr()
        assert error_message in captured.err
        assert e.code == 1
    else:
        assert False, "log_error did not raise a SystemExit exception"


def test_get_user_by_email(monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 200

            def raise_for_status(self):
                pass

            def json(self):
                return {"email": "test@mail"}

        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    server_url = "http://test.com"
    token = "test_token"

    user = get_user_by_email(server_url, token, "test@mail")
    assert user == {"email": "test@mail"}


def test_get_user_by_email_failed(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.exceptions.RequestException()

    monkeypatch.setattr(requests, "get", mock_get)

    email = "test@mail"
    server_url = "http://test.com"
    token = "test_token"
    error_message = (
        f"Error getting user by email: GET http://test.com/api/v4/users/email/{email}"
    )

    with pytest.raises(APICallError) as e:
        get_user_by_email(server_url, token, email)

    assert (
        str(e.value) == error_message
    ), f"Expected: {error_message}, got: {str(e.value)}"


def test_get_user_by_username(monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 200

            def raise_for_status(self):
                pass

            def json(self):
                return {"username": "test_user"}

        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    server_url = "http://test.com"
    token = "test_token"

    user = get_user_by_email(server_url, token, "test_user")
    assert user == {"username": "test_user"}


def test_get_user_by_username_failed(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.exceptions.RequestException()

    monkeypatch.setattr(requests, "get", mock_get)

    username = "test_user"
    server_url = "http://test.com"
    token = "test_token"
    error_message = f"Error getting user by username: GET http://test.com/api/v4/users/username/{username}"

    with pytest.raises(APICallError) as e:
        get_user_by_username(server_url, token, username)

    assert (
        str(e.value) == error_message
    ), f"Expected: {error_message}, got: {str(e.value)}"


def test_send_message(monkeypatch):
    def mock_post(*args, **kwargs):
        class MockResponse:
            status_code = 200

            def raise_for_status(self):
                pass

            def json(self):
                return {"channel_id": "test_channel_id"}

        return MockResponse()

    monkeypatch.setattr(requests, "post", mock_post)

    server_url = "http://test.com"
    token = "test_token"
    channel_id = "test_channel_id"
    message = "test_message"

    response = send_message(server_url, token, channel_id, message)
    assert response == {"channel_id": "test_channel_id"}


def test_create_direct_channel(monkeypatch):
    def mock_post(*args, **kwargs):
        class MockResponse:
            status_code = 200

            def raise_for_status(self):
                pass

            def json(self):
                return {"id": "test_channel_id"}

        return MockResponse()

    monkeypatch.setattr(requests, "post", mock_post)

    server_url = "http://test.com"
    token = "test_token"
    user1_id = "test_user1_id"
    user2_id = "test_user2_id"

    response = create_direct_channel(server_url, token, user1_id, user2_id)
    assert response == {"id": "test_channel_id"}


def test_get_me(monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 200

            def raise_for_status(self):
                pass

            def json(self):
                return {"username": "me"}

        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    server_url = "http://test.com"
    token = "test_token"

    user = get_me(server_url, token)
    assert user == {"username": "me"}


def test_get_me_failed(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.exceptions.RequestException()

    monkeypatch.setattr(requests, "get", mock_get)

    server_url = "http://test.com"
    token = "test_token"
    error_message = f"Error getting current user: GET http://test.com/api/v4/users/me"

    with pytest.raises(APICallError) as e:
        get_me(server_url, token)

    assert (
        str(e.value) == error_message
    ), f"Expected: {error_message}, got: {str(e.value)}"
