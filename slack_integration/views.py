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

from slack_integration.models import HomeOffice
from slack.signature import SignatureVerifier
signature_verifier = SignatureVerifier(os.environ["SLACK_SIGNING_SECRET"])

slack_token = os.environ["SLACK_API_TOKEN"]
client = WebClient(token=slack_token)

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
        ModalsHandler.open_add_modal(request.POST["trigger_id"])

    if command_text == "today":
        return JsonResponse(InteractionHandler.handle_add_request_from_command(request, date.today().strftime('%Y-%m-%d')))
    
    if command_text == "tomorrow":
        return JsonResponse(InteractionHandler.handle_add_request_from_command(request, (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')))

    return HttpResponse("")

@csrf_exempt
def interaction(request):
    return JsonResponse(InteractionHandler.handle_interaction_request(request))






