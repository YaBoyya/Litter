# Generated by Django 4.2.6 on 2023-10-29 18:09

from django.db import migrations
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='litteruser',
            managers=[
                ('objects', users.models.LitterUserManager()),
            ],
        ),
    ]
