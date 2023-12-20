import os
import sys
from mattermost import read_message, send, is_empty, log_error


def main():
    msg = {}

    mattermost_msg = os.getenv("MATTERMOST_MESSAGE")
    if mattermost_msg is not None:
        msg["text"] = mattermost_msg
    else:
        msg = read_message("mattermost.json")

    webhook = os.getenv("MATTERMOST_WEBHOOK_URL")
    if not webhook:
        log_error("Missing MATTERMOST_WEBHOOK_URL environment variable")

    channel_name = os.getenv("MATTERMOST_CHANNEL", msg.get("ChannelName", ""))
    if channel_name is not None:
        msg["ChannelName"] = channel_name

    username = os.getenv("MATTERMOST_USERNAME", msg.get("Username", ""))
    if username is not None:
        msg["Username"] = username

    icon_url = os.getenv("MATTERMOST_ICON", msg.get("IconURL", ""))
    if icon_url is not None:
        msg["IconURL"] = icon_url

    if is_empty(msg):
        print(
            "mattermost.json and MATTERMOST_MESSAGE  is empty, exiting without failing."
        )
        sys.exit(0)

    send(webhook, msg)
    print("Mattermost message sent!")


if __name__ == "__main__":
    main()
