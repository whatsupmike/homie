from slack.errors import SlackApiError
from slack import WebClient
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
from slack.signature import SignatureVerifier
signature_verifier = SignatureVerifier(os.environ["SLACK_SIGNING_SECRET"])

slack_token = os.environ["SLACK_API_TOKEN"]
client = WebClient(token=slack_token)

@csrf_exempt
def command(request):
    if not signature_verifier.is_valid_request(request.body, request.headers):
        return HttpResponse("invalid request", status=403)

    client.views_open(
        trigger_id=request.POST["trigger_id"],
        view={
            "type": "modal",
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
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Since when?"
                    },
                    "accessory": {
                        "type": "datepicker",
                        "placeholder": {
                                "type": "plain_text",
                                "text": "Select a date",
                                "emoji": True
                        },
                        "action_id": "datepicker-action"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Till when?"
                    },
                    "accessory": {
                        "type": "datepicker",
                        "placeholder": {
                                "type": "plain_text",
                                "text": "Select a date",
                                "emoji": True
                        },
                        "action_id": "datepicker-action"
                    }
                }
            ]
        }
    )

    return HttpResponse("")
