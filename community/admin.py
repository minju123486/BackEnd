from django.contrib import admin

# Register your models here.
from .models import post, comment
# Register your models here.
admin.site.register(post)
admin.site.register(comment)