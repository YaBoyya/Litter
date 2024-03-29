# Generated by Django 4.2.7 on 2023-12-30 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_comment_post_commentvote_unique_comment_vote__and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='total_votes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='total_votes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='commentvote',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentvote', to='core.comment'),
        ),
        migrations.AlterField(
            model_name='postvote',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postvote', to='core.post'),
        ),
    ]
