# Generated by Django 4.1 on 2022-09-12 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0002_user_is_agent_user_is_organisor'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agent',
            old_name='User',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='user',
            new_name='User',
        ),
    ]