from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import notice_submission
from accounts.models import CustomUser
from django.core.mail import send_mail


@receiver(pre_save, sender=notice_submission)
def track_status_change(sender, instance, **kwargs):
    if instance.pk:
        previous = sender.objects.get(pk=instance.pk)
        instance._original_status = previous.status


@receiver(post_save, sender=notice_submission)
def notice_submission_status_change(sender, instance, created, **kwargs):
    print("Came hereeee")
    if created:
        print("ITS HAPPENING")
        if instance.status == 'published':
            send_info(instance)
    else:
        if hasattr(instance, '_original_status') and instance._original_status != instance.status:
            print(f"THE STATUS is changed to  {instance.status}")
            if instance.status == 'published':
                send_info(instance)


from django.conf import settings
from django.core.mail import EmailMessage


def send_info(information):
    local_gov = information.Uploader.Local_government

    target_consumers = CustomUser.objects.filter(Local_government=local_gov)
    for char in target_consumers:

        email = EmailMessage(
            'New offer for you',
            f'Hello {char.Name}\n\n {information.Uploader.Name} has uploaded new agriculture scheme available in your area.',
            f'{settings.EMAIL_HOST_USER}',
            [char.email]

        )
        email.attach_file(information.notice.path)
        email.send()

        print("Email sent")
