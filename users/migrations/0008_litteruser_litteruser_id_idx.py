# Generated by Django 4.2.7 on 2024-01-05 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_litteruser_options_alter_litteruser_usertag_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='litteruser',
            index=models.Index(fields=['id'], name='litteruser_id_idx'),
        ),
    ]
