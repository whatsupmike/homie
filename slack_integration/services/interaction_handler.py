from datetime import datetime, date, timedelta
from slack_integration.models import HomeOffice
import os
import json
from slack import WebClient
from slack.signature import SignatureVerifier

from slack_integration.services.request_validator import RequestValidator

signature_verifier = SignatureVerifier(os.environ["SLACK_SIGNING_SECRET"])
slack_token = os.environ["SLACK_API_TOKEN"]
client = WebClient(token=slack_token)

class InteractionHandler:
    @classmethod
    def handle_interaction_request(self, request):
        if not RequestValidator.validate_interaction_request(request):
            return self.error_response_json("Invalid Request")

        payload = self.get_payload_from_request(request)
        callback_id = payload["view"]["callback_id"]

        if(callback_id == "add_request"):
            return self.process_add_request_from_payload(payload)

        if(callback_id == "edit_request"):
            return {}

        return {}

    @classmethod
    def handle_add_request_from_command(self, request, day):
        user = self.get_user_from_request(request)
        validate_result = self.validate_and_save_add_request(user, day, day)
        if not validate_result["ok"]:
            return self.message_json(":x: " + validate_result["message"])

        self.notify_on_new_request(user, day, day)

        return self.message_json(":white_check_mark: Successfully requested")

    @classmethod
    def process_add_request_from_payload(self, payload):
        if payload["type"] == "view_submission":
            values = payload["view"]["state"]["values"]
            since = self.get_date_from_values(values, "datepicker-since-action")
            till = self.get_date_from_values(values, "datepicker-till-action")
            user = payload["user"]

            validate_result = self.validate_and_save_add_request(user, since, till)
            if not validate_result["ok"]:
                return self.error_response_json(validate_result["message"])

            self.notify_on_new_request(user, since, till)

        return {}

    @classmethod
    def validate_and_save_add_request(self, user, since, till):
        if since > till or since < date.today().strftime('%Y-%m-%d'):
            return self.validation_message_to_object(False, "Invalid Date")

        if RequestValidator.validate_user_other_ho_requests(user["id"], since, till):
            return self.validation_message_to_object(False, "Date already requested")

        #   Additional user data
        user_response = client.users_profile_get(user=user["id"])
        if not user_response["ok"]:
            return self.validation_message_to_object(False, "Invalid User")

        ho = HomeOffice(user_id=user["id"], user_name=user["username"], since=since, till=till)
        ho.save()

        return self.validation_message_to_object(True, "Success")

    @classmethod
    def notify_on_new_request(self, user, since, till):
        client.chat_postMessage(
                channel=os.environ["SLACK_CHANNEL"], text=self.success_message_text(user["username"], since, till), link_names=1)

    @classmethod
    def get_date_from_values(self, values, action_id):
        for key, value in values.items():
            if action_id in value:
                return value[action_id]["selected_date"]
    
    @classmethod
    def success_message_text(self, username, since, till):
        return "@" + username + " requested for home office. *" + since + "* - *" + till + "*"

    @classmethod
    def error_response_json(self, text):
        return {
            "response_action": "errors",
            "errors": {
                "datepicker-till": text
            }
        }
    
    @classmethod
    def validation_message_to_object(self, ok, text):
        return {
            "ok": ok,
            "message": text
        }

    @classmethod
    def get_payload_from_request(self, request):
        return json.loads(request.POST.get("payload", False))

    @classmethod
    def get_user_from_request(self, request):
        if request.POST.get("user_id", False):
            return {
                "id": request.POST["user_id"],
                "username": request.POST["user_name"]
            }
        payload = self.get_payload_from_request(request)

        return payload["user"]
    
    @classmethod
    def message_json(self, message):
        return {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": message
                    }
                }
            ]
        }
