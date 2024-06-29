from django.contrib.auth.models import AbstractUser
from django.db import models


from .managers import UserManager


class CustomUser(AbstractUser):

    username = None
    email = models.EmailField(max_length=100, null=True)
    Name = models.CharField(max_length=150)
    Contact_no = models.CharField(max_length=100, unique=True)
    Province = models.CharField(max_length=100)
    District = models.CharField(max_length=100)
    Local_government = models.CharField(max_length=100)
    # user_type = models.CharField(max_length=100, default='farmer')
    identity_proof = models.ImageField(upload_to='proof_document/')
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'Contact_no'
    REQUIRED_FIELDS = ()



    FARMER_USER = 'Farmer'
    OFFICIAL_USER = 'Official'

    STATUS_CHOICES = [
        (FARMER_USER, 'FARMER'),
        (OFFICIAL_USER, 'Official'),

    ]
    user_type = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=FARMER_USER,
    )

    objects = UserManager()

    def __str__(self):
        return self.Name


class official_requests(models.Model):
    Name = models.CharField(max_length=150)
    Contact_no = models.CharField(max_length=100, unique=True)
    email=models.EmailField(max_length=100,default='none')
    Province = models.CharField(max_length=100)
    District = models.CharField(max_length=100)
    Local_government = models.CharField(max_length=100)
    password=models.CharField(max_length=100,default='<PASSWORD>')

    identity_proof = models.ImageField(upload_to='pending_official_requests/')
    date = models.DateTimeField(auto_now_add=True)

    STATUS_WAITING = 'waiting'
    STATUS_ACCEPTED = 'accepted'
    STATUS_REJECTED_or_deleted = 'rejected'


    STATUS_CHOICES = [
        (STATUS_WAITING, 'Waiting'),
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_REJECTED_or_deleted, 'Rejected'),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_WAITING,
    )

