import os

command_name = os.environ["SLACK_COMMAND_NAME"]

class MessageService:
    @classmethod
    def get_help_message_json(self):
        return {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": "Need help? I'm there for You! :house_with_garden:",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": "Homie is simple :slack: app for requesting Home Office.",
                        "emoji": True
                    }
                },
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": ":book: Available commands:",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "`" + command_name + "` *or* `" + command_name + " new` :\nModal would pop up where You would be able to select dates and send home office request to Your supervisor"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "`" + command_name + " today` :\nShortcut to request HO for today"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "`" + command_name + " tomorrow` :\nShortcut to request HO for tomorrow"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "`" + command_name + " list` :\nList all HO requests 3 weeks back"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "`" + command_name + " list today` :\nList all HO requests for today"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "`" + command_name + " help` :\nHelp! Duhhhh!"
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": "Still needs some help?\nTry here https://github.com/whatsupmike/homie also feel free to contribute! "
                        }
                    ]
                }
            ]
        }
