# Generated by Django 4.2.6 on 2023-11-01 16:32

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_language_remove_post_language_post_languages'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='picture',
            field=models.ImageField(null=True, upload_to=core.models.PathAndRename('post_pictures/')),
        ),
    ]
