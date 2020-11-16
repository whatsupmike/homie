from datetime import datetime, date, timedelta
from slack_integration.models import HomeOffice

class ListService:
    @classmethod
    def get_users_recently_on_ho(self):
        delta = timedelta(days=21)
        users_on_ho = HomeOffice.objects.all().filter(till__gte=date.today()-delta).order_by('user_id', 'since')

        return self.format_list_message(self.ho_to_array(users_on_ho))

    @classmethod
    def get_users_today_on_ho(self):
        users_on_ho = HomeOffice.objects.filter(since__lte=date.today(), till__gte=date.today())

        return self.format_list_message(self.ho_to_array(users_on_ho))
    
    @classmethod
    def ho_to_array(self, ho_objects):
        value = {}
        for ho in ho_objects.values():
            if not ho["user_id"] in value:
                value[ho["user_id"]] = ""

            value[ho["user_id"]] += "*" + str(ho["since"]) + " - " + str(ho["till"]) + "*\n"
        return value

    @classmethod
    def format_list_message(self, users_array):
        blocks = []
        for key, value in users_array.items():
            blocks.append({
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": self.get_user_mention_string(key) 
                    },
                    {
                        "type": "mrkdwn",
                        "text": value
                    }
                ]
            })

        return {
            "blocks": blocks
        }

    @classmethod
    def get_user_mention_string(self, user_id):
        return "<@" + user_id + ">"
