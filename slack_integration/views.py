from slack.errors import SlackApiError
from slack import WebClient
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json

from datetime import datetime, date
from collections import namedtuple

from slack_integration.models import HomeOffice
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
    )

    return HttpResponse("")

@csrf_exempt
def interaction(request):
    if not validate_interaction_request(request):
        return JsonResponse(interaction_response("Invalid Request"))

    payload = json.loads(request.POST["payload"])

    if payload["type"] == "view_submission":
        values = payload["view"]["state"]["values"]
        since = get_date_from_values(values, "datepicker-since-action")
        till = get_date_from_values(values, "datepicker-till-action")
        user = payload["user"]

        if since > till or since < date.today().strftime('%Y-%m-%d'):
            return JsonResponse(interaction_response("Invalid Date"))

        if validate_user_other_ho_requests(user["id"], since, till):
            return JsonResponse(interaction_response("Date already requested"))

        #   Additional user data
        user_response = client.users_profile_get(user=user["id"])
        if not user_response["ok"]:
            return JsonResponse(interaction_response("Invalid User"))

        ho = HomeOffice(user_id=user["id"], since=since, till=till)
        ho.save()
        client.chat_postMessage(
            channel=os.environ["SLACK_CHANNEL"], text=success_message_text(ho, user["username"]), link_names=1)

    return JsonResponse({})

def validate_interaction_request(request):
    if not signature_verifier.is_valid_request(request.body, request.headers):
        return False

    if not "payload" in request.POST:
        return False

    payload = json.loads(request.POST["payload"])

    if not "type" in payload:
        return False

    return True

def get_date_from_values(values, action_id):
    for key, value in values.items():
        if action_id in value:
            return value[action_id]["selected_date"]


def interaction_response(text):
    return {
        "response_action": "errors",
        "errors": {
            "datepicker-till": text
        }
    }

def success_message_text(ho, username):
    return "@" + username + " requested for home office. *" + ho.since + "* - *" + ho.till + "*"

def validate_user_other_ho_requests(user_id, since, till):
    ho_requests = get_user_ho_requests(user_id)
    for ho in ho_requests.values():
        if validate_date_overlaping(ho, since, till):
            return True
    return False

def get_user_ho_requests(user_id):
    return HomeOffice.objects.filter(since__gte=date.today(), user_id__startswith=user_id)

def validate_date_overlaping(ho, start_date, end_date):
    Range = namedtuple('Range', ['start', 'end'])

    r1 = Range(start=get_datetime_from_string(start_date), end=get_datetime_from_string(end_date))
    r2 = Range(start=ho["since"], end=ho["till"])

    latest_start = max(r1.start, r2.start)
    earliest_end = min(r1.end, r2.end)

    delta = (earliest_end - latest_start).days + 1

    return delta > 0

def get_datetime_from_string(datetime_string):
    return datetime.strptime(datetime_string, '%Y-%m-%d').date()
