# Generated by Django 4.2.7 on 2024-01-06 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_post_post_id_idx_post_post_desc_created_idx_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['created'], name='post_created_idx'),
        ),
    ]