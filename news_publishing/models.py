from django.db import models
from accounts.models import CustomUser



# Create your models here.
class notice_submission(models.Model):
    Uploader=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    notice=models.ImageField(upload_to='submitted_notices/',blank=False,null=False)
    date_submitted = models.DateTimeField(auto_now_add=True)

    STATUS_WAITING = 'waiting'
    STATUS_PUBLISHED= 'published'


    STATUS_CHOICES = [
        (STATUS_WAITING, 'WAITING'),
        (STATUS_PUBLISHED, 'PUBLISHED'),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_WAITING,
    )



class scoreboard(models.Model):
    User = models.OneToOneField(CustomUser, on_delete=models.CASCADE,unique=True,related_name='scoreboard_track')
    Score= models.IntegerField(default=0)

