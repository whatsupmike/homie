from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
from slack.signature import SignatureVerifier
signature_verifier = SignatureVerifier(os.environ["SLACK_SIGNING_SECRET"])

@csrf_exempt
def command(request):
    if not signature_verifier.is_valid_request(request.body, request.headers):
        return HttpResponse("invalid request", status=403)

    return HttpResponse("Success")
