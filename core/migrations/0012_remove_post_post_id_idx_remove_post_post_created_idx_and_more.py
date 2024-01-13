# Generated by Django 4.2.7 on 2024-01-13 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_post_post_created_idx'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='post',
            name='post_id_idx',
        ),
        migrations.RemoveIndex(
            model_name='post',
            name='post_created_idx',
        ),
        migrations.RemoveIndex(
            model_name='postvote',
            name='postvote_post_idx',
        ),
        migrations.RemoveIndex(
            model_name='postvote',
            name='postvote_user_idx',
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['-total_votes'], name='post_created_idx'),
        ),
    ]
