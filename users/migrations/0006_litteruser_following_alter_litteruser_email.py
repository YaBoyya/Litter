# Generated by Django 4.2.6 on 2023-11-22 12:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_litteruser_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='litteruser',
            name='following',
            field=models.ManyToManyField(related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='litteruser',
            name='email',
            field=models.EmailField(error_messages={'unique': 'This email has already been registered.'}, max_length=254, verbose_name='email address'),
        ),
    ]