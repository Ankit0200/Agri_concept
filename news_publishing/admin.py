from django.contrib import admin
from .models import notice_submission,scoreboard

# Register your models here.
admin.site.register(notice_submission)
admin.site.register(scoreboard)