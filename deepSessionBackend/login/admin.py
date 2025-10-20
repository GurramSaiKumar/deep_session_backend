# Register your models here.
from django.contrib import admin

from .models import NewUser, NewOTP

admin.site.register(NewUser)
admin.site.register(NewOTP)
