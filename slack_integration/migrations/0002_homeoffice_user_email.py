# Generated by Django 3.1.2 on 2020-11-15 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slack_integration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='homeoffice',
            name='user_name',
            field=models.CharField(default="", max_length=100),
            preserve_default=False,
        ),
    ]