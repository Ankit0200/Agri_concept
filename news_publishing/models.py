from django.db import models
from accounts.models import CustomUser

# Create your models here.
class notice_submission(models.Model):
    Uploader=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    notice=models.ImageField(upload_to='submitted_notices/',blank=False,null=False)
