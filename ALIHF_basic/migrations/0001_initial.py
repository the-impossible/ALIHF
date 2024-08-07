# Generated by Django 5.0.7 on 2024-07-25 01:55

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="WebinarVideos",
            fields=[
                (
                    "webinar_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("webinar_title", models.CharField(max_length=100)),
                ("video_id", models.CharField(max_length=100)),
                ("date_created", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name_plural": "Webinar Videos",
                "db_table": "Webinar Videos",
            },
        ),
    ]
