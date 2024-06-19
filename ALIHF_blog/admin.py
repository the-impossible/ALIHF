from django.contrib import admin
from ALIHF_blog.models import *

# Register your models here.
class BlogPostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}


admin.site.register(BlogPost, BlogPostAdmin)