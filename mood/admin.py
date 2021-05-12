from django.contrib import admin
from mood.models import *
from django.contrib.auth.admin import UserAdmin


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Bio)
admin.site.register(Privacy)
