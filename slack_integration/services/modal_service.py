from datetime import datetime, date, timedelta
from slack_integration.models import HomeOffice
import os
from slack import WebClient

slack_token = os.environ["SLACK_API_TOKEN"]
client = WebClient(token=slack_token)

class ModalService:
    @classmethod
    def open_add_modal(self, trigger_id):
        self.open_modal(trigger_id, self.get_modal_json_for_new_request())

    @classmethod
    def open_delete_modal(self, trigger_id, user_id):
        user_on_ho = HomeOffice.objects.filter(
            till__gte=date.today(), user_id=user_id)
        
        if user_on_ho.count() == 0:
            return False

        self.open_modal(trigger_id, self.get_modal_json_for_delete_request(user_on_ho))

        return True

    @classmethod
    def open_modal(self, trigger_id, json):
        client.views_open(
            trigger_id=trigger_id,
            view=json
        )

    @classmethod
    def get_modal_json_for_new_request(self):
        return {
            "type": "modal",
            "callback_id": "add_request",
            "title": {
                "type": "plain_text",
                "text": "Want to work from home?",
                "emoji": True
            },
            "submit": {
                "type": "plain_text",
                "text": "Submit",
                "emoji": True
            },
            "close": {
                "type": "plain_text",
                "text": "Cancel",
                "emoji": True
            },
            "blocks": [
                {
                    "type": "input",
                    "block_id": "datepicker-since",
                    "element": {
                        "type": "datepicker",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a date",
                            "emoji": True
                        },
                        "action_id": "datepicker-since-action"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Since when?",
                        "emoji": True
                    }
                },
                {
                    "type": "input",
                    "block_id": "datepicker-till",
                    "element": {
                        "type": "datepicker",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a date",
                            "emoji": True
                        },
                        "action_id": "datepicker-till-action"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Till when?",
                        "emoji": True
                    }
                }
            ]
        }

    @classmethod
    def get_modal_json_for_delete_request(self, user_on_ho):
        options = []

        for ho in user_on_ho.values():
            options.append({
                "text": {
                    "type": "mrkdwn",
                    "text": "*" + str(ho["since"]) + " - " + str(ho["till"]) + "*"
                },
                "value": str(ho["id"])
            })

        return {
            "type": "modal",
            "callback_id": "delete_request",
            "title": {
                "type": "plain_text",
                "text": "Delete requests",
                "emoji": True
            },
            "submit": {
                "type": "plain_text",
                "text": "Submit",
                "emoji": True
            },
            "close": {
                "type": "plain_text",
                "text": "Cancel",
                "emoji": True
            },
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": ":wastebasket: Select requests to delete:"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "checkboxes",
                            "options": options,
                            "action_id": "delete-ho-request"
                        }
                    ]
                }
            ]
        }
