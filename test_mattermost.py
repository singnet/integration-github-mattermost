import io
import requests
import json
from unittest.mock import patch, mock_open
from mattermost import read_message, send, is_empty, log_error


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
