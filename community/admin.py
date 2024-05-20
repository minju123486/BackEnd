from django.contrib import admin

# Register your models here.
from .models import post, comment, like_check, grade_search
# Register your models here.
admin.site.register(post)
admin.site.register(comment)
admin.site.register(like_check)
admin.site.register(grade_search)