# Generated by Django 5.0.6 on 2024-05-20 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djapp', '0002_user_is_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
