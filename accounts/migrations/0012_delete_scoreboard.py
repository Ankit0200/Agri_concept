# Generated by Django 5.0.6 on 2024-06-28 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_customuser_email'),
    ]

    operations = [
        migrations.DeleteModel(
            name='scoreboard',
        ),
    ]