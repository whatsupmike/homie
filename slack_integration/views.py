from slack.errors import SlackApiError
from slack import WebClient
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json

from datetime import datetime, date, timedelta
from collections import namedtuple

from slack_integration.services.list_service import ListService
from slack_integration.services.modal_service import ModalService
from slack_integration.services.interaction_handler import InteractionHandler
from slack_integration.services.message_service import MessageService

from slack_integration.models import HomeOffice
from slack.signature import SignatureVerifier
signature_verifier = SignatureVerifier(os.environ["SLACK_SIGNING_SECRET"])

slack_token = os.environ["SLACK_API_TOKEN"]
client = WebClient(token=slack_token)

command_name = os.environ["SLACK_COMMAND_NAME"]

@csrf_exempt
def command(request):
    if not signature_verifier.is_valid_request(request.body, request.headers):
        return HttpResponse("invalid request", status=403)

    command_text = request.POST["text"]
    if command_text == "list":
        return JsonResponse(ListService.get_users_recently_on_ho())
    
    if command_text == "list today":
        return JsonResponse(ListService.get_users_today_on_ho())
    
    if not command_text or command_text == "new":
        ModalService.open_add_modal(request.POST["trigger_id"])

        return HttpResponse("")

    if command_text == "today":
        return JsonResponse(InteractionHandler.handle_add_request_from_command(request, date.today().strftime('%Y-%m-%d')))
    
    if command_text == "tomorrow":
        return JsonResponse(InteractionHandler.handle_add_request_from_command(request, (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')))

    if command_text == "delete":
        user = InteractionHandler.get_user_from_request(request)
        is_valid = ModalService.open_delete_modal(request.POST["trigger_id"], user["id"])

        return HttpResponse("" if is_valid else "Nothing to edit")

    return JsonResponse(MessageService.get_help_message_json())

@csrf_exempt
def interaction(request):
    return JsonResponse(InteractionHandler.handle_interaction_request(request))






