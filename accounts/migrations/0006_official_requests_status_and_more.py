# Generated by Django 5.0.3 on 2024-06-20 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_official_requests_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='official_requests',
            name='status',
            field=models.CharField(choices=[('waiting', 'Waiting'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='waiting', max_length=10),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]