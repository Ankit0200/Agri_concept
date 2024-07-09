from django.contrib import admin
from .models import CustomUser,official_requests,Province,District,LocalBody
admin.site.register(CustomUser)
admin.site.register(official_requests)

admin.site.register(Province)
admin.site.register(District)
admin.site.register(LocalBody)



# Register your models here.
