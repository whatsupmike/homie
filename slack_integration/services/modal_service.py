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
    def open_edit_modal(self, trigger_id):
        self.open_modal(trigger_id, self.get_modal_json_for_edit_request())

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
    def get_modal_json_for_edit_request(self):
        return {} 
        