# Integration Github Mattermost

GitHub Actions for sending messages to Mattermost.

## Environment Variables

| Variable               | Purpose                                                                                                                                              | Optional |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| MATTERMOST_WEBHOOK_URL | The Mattermost Incoming Webhook URL.                                                                                                                 | No       |
| MATTERMOST_CHANNEL     | The name of the channel where you want to post messages. If not specified, the message will be posted in the channel set up in the webhook creation. | Yes      |
| MATTERMOST_USERNAME    | The name of the sender of the message, for example, "GitHubAction".                                                                                  | Yes      |
| MATTERMOST_ICON        | The user or bot icon shown with the Mattermost message.                                                                                              | Yes      |

## Action Example

```yaml
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Notify Mattermost
        uses: singnet/integration-github-mattermost@master
        env:
          MATTERMOST_WEBHOOK_URL: ${{ secrets.MATTERMOST_WEBHOOK_URL }}
          MATTERMOST_CHANNEL: ${{ secrets.MATTERMOST_CHANNEL }}
          MATTERMOST_USERNAME: "GitHubAction"
          MATTERMOST_ICON: "https://example.com/icon.png"
```
