from django.db import models
import uuid

# Create your models here.
class WebinarVideos(models.Model):

    webinar_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    webinar_speaker = models.CharField(max_length=100)
    webinar_title = models.CharField(max_length=100)
    video_id = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.webinar_title} : {self.video_id}"

    class Meta:
        db_table = 'Webinar Videos'
        verbose_name_plural = 'Webinar Videos'