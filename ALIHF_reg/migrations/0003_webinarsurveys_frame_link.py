# Generated by Django 5.0.6 on 2024-07-20 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ALIHF_reg", "0002_webinarsurveys"),
    ]

    operations = [
        migrations.AddField(
            model_name="webinarsurveys",
            name="frame_link",
            field=models.URLField(blank=True),
        ),
    ]
