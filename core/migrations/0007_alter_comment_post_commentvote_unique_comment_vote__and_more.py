# Generated by Django 4.2.6 on 2023-11-09 08:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_post_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='core.post'),
        ),
        migrations.AddConstraint(
            model_name='commentvote',
            constraint=models.UniqueConstraint(fields=('user', 'comment'), name='Unique comment vote.'),
        ),
        migrations.AddConstraint(
            model_name='postvote',
            constraint=models.UniqueConstraint(fields=('user', 'post'), name='Unique post vote.'),
        ),
    ]