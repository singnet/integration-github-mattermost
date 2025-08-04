import os

from mattermost import is_empty, log_error, read_message, send_message, upload_files


def require_env(var_name: str, msg_dict=None) -> str:
    value = os.getenv(
        var_name,
        msg_dict.get(var_name.replace("MATTERMOST_", ""), "") if msg_dict else "",
    )
    if not value or not str(value).strip():
        log_error(f"{var_name} is required and cannot be empty.")
    return value.strip()


def main():
    msg = {}

    mattermost_msg = os.getenv("MATTERMOST_MESSAGE")
    if mattermost_msg and mattermost_msg.strip():
        msg["text"] = mattermost_msg.strip()
    else:
        msg = read_message("mattermost.json")

    server_url = require_env("MATTERMOST_SERVER_URL", msg)
    token = require_env("MATTERMOST_TOKEN", msg)
    channel_id = require_env("MATTERMOST_CHANNEL_ID", msg)

    attachments_path = os.getenv(
        "MATTERMOST_ATTACHMENTS_PATH", msg.get("AttachmentsPath", "")
    ).strip()
    file_ids = []
    if attachments_path:
        paths = [p.strip() for p in attachments_path.split(",") if p.strip()]
        if not paths:
            log_error(
                "MATTERMOST_ATTACHMENTS_PATH is defined but contains no valid paths."
            )
        file_ids = upload_files(server_url, token, channel_id, paths)

    if is_empty(msg) or not msg.get("text", "").strip():
        log_error("Message text is required (MATTERMOST_MESSAGE or mattermost.json).")

    send_message(server_url, token, channel_id, msg["text"], file_ids)
    print("Mattermost message sent!")


if __name__ == "__main__":
    main()
