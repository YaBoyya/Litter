# Generated by Django 4.2.6 on 2023-11-09 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_litteruser_email_userfollowing'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='userfollowing',
            constraint=models.UniqueConstraint(fields=('user', 'followed_user'), name='unique_followers'),
        ),
    ]
