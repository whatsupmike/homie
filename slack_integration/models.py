from django.db import models

# Create your models here.

class HomeOffice(models.Model):
    user_id = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    since = models.DateField()
    till = models.DateField()

    def __str__(self):
        return self.user_id + ": " + self.since + " -> " + self.till
