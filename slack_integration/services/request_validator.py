from datetime import datetime, date
from collections import namedtuple
import os
import json
from slack_integration.models import HomeOffice

from slack.signature import SignatureVerifier
signature_verifier = SignatureVerifier(os.environ["SLACK_SIGNING_SECRET"])

class RequestValidator:
    @classmethod
    def validate_interaction_request(self, request):
        if not signature_verifier.is_valid_request(request.body, request.headers):
            return False

        if not "payload" in request.POST:
            return False

        payload = json.loads(request.POST["payload"])

        if not "type" in payload:
            return False

        return True

    @classmethod
    def validate_date_overlaping(self, ho, start_date, end_date):
        Range = namedtuple('Range', ['start', 'end'])

        r1 = Range(start=self.get_datetime_from_string(start_date), end=self.get_datetime_from_string(end_date))
        r2 = Range(start=ho["since"], end=ho["till"])

        latest_start = max(r1.start, r2.start)
        earliest_end = min(r1.end, r2.end)

        delta = (earliest_end - latest_start).days + 1

        return delta > 0

    @classmethod
    def get_datetime_from_string(self, datetime_string):
        return datetime.strptime(datetime_string, '%Y-%m-%d').date()

    @classmethod
    def validate_user_other_ho_requests(self, user_id, since, till):
        ho_requests = self.get_user_ho_requests(user_id)
        for ho in ho_requests.values():
            if self.validate_date_overlaping(ho, since, till):
                return True
        return False

    @classmethod
    def get_user_ho_requests(self, user_id):
        return HomeOffice.objects.filter(since__gte=date.today(), user_id__startswith=user_id)
