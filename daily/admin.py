from django.contrib import admin
from .models import daily_user, daily_model, daily_class
# Register your models here.
admin.site.register(daily_model)
admin.site.register(daily_user)
admin.site.register(daily_class)