import json
import requests
import sys


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


def is_empty(msg):
    return not bool(msg)


def log_error(message):
    print(message, file=sys.stderr)
    sys.exit(1)
