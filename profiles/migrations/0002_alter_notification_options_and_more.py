# Generated by Django 4.2.6 on 2023-11-19 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ['-time_sent']},
        ),
        migrations.AlterField(
            model_name='notification',
            name='activity_type',
            field=models.CharField(choices=[('comment', 'has commented on your post.'), ('follow', 'has followed you.')], verbose_name='Activity Type'),
        ),
    ]
