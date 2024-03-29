# Generated by Django 4.2.6 on 2023-10-30 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_comment_options_alter_post_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={},
        ),
        migrations.AddField(
            model_name='comment',
            name='was_edited',
            field=models.BooleanField(default=False, verbose_name='Was edited'),
        ),
        migrations.AddField(
            model_name='post',
            name='was_edited',
            field=models.BooleanField(default=False, verbose_name='Was edited'),
        ),
    ]
