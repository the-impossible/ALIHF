from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
import uuid

# Create your models here.
class BlogPost(models.Model):
    blog_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    title = models.CharField(max_length=500)
    body = CKEditor5Field(config_name='extends')
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title