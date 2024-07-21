from django.db import models
from accounts.models import CustomUser



# Create your models here.
class notice_submission(models.Model):
    notice_title=models.CharField(max_length=200,null=False,default='null')
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
    sent_in_phone=models.BooleanField(default=False)


    def save(self, *args, **kwargs):

        if self.pk is not None:
            original_status = notice_submission.objects.get(pk=self.pk).status
            if original_status == self.STATUS_PUBLISHED and self.status != self.STATUS_PUBLISHED:
                raise ValueError("Cannot change the status once it has been published.")

        super(notice_submission, self).save(*args, **kwargs)



class scoreboard(models.Model):
    User = models.OneToOneField(CustomUser, on_delete=models.CASCADE,unique=True,related_name='scoreboard_track')
    Score= models.IntegerField(default=0)

