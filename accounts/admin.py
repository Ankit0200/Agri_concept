from django.contrib import admin
from .models import CustomUser,official_requests
admin.site.register(CustomUser)
admin.site.register(official_requests)

# Register your models here.
