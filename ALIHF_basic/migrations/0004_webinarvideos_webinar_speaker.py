# Generated by Django 5.0.7 on 2024-07-25 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ALIHF_basic", "0003_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="webinarvideos",
            name="webinar_speaker",
            field=models.CharField(default="", max_length=100),
            preserve_default=False,
        ),
    ]