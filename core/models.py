import os
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from .managers import PostManager


@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = f'{uuid4()}.{ext}'
        return os.path.join(self.path, filename)


class Language(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey('users.LitterUser', on_delete=models.CASCADE)
    languages = models.ManyToManyField(Language)
    title = models.CharField(_("Title"), max_length=100)
    text = models.TextField(_("Description"), max_length=500, null=True,
                            blank=True)
    picture = models.ImageField(upload_to=PathAndRename('post_pictures/'),
                                null=True)
    total_votes = models.IntegerField(default=0)
    DIFFICULTY = [
        ('E', 'Easy'),
        ('M', 'Medium'),
        ('H', 'Hard'),
    ]
    difficulty = models.CharField(_("Difficulty"), choices=DIFFICULTY,
                                  null=True)
    views = models.IntegerField(_("Views"), default=0)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    was_edited = models.BooleanField(_('Was edited'), default=False)

    objects = PostManager()

    class Meta:
        indexes = [
            models.Index(fields=['user'], name='post_user_idx'),
        ]

    def __str__(self):
        return f'{self.text[:50]}...' if len(self.title) > 50 else self.title

    def delete(self, *args, **kwargs):
        if self.picture:
            root = settings.MEDIA_ROOT
            relative_path = str(self.picture).replace("/", "\\")
            absolute_path = os.path.join(root, relative_path)
            os.remove(absolute_path)
        super().delete(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey('users.LitterUser', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comment',
                             on_delete=models.CASCADE)
    text = models.CharField(_("Text"), max_length=200)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    was_edited = models.BooleanField(_('Was edited'), default=False)
    total_votes = models.IntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['user'], name='comment_user_idx'),
            models.Index(fields=['post'], name='comment_post_idx')
        ]

    def __str__(self):
        return f'{self.text[:50]}...' if len(self.text) > 50 else self.text


class PostVote(models.Model):
    user = models.ForeignKey('users.LitterUser', on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Post, related_name='postvote',
                             on_delete=models.CASCADE)
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'],
                                    name="Unique post vote.")
            ]
        indexes = [
            models.Index(fields=['user', 'post'],
                         name="postvote_user_post_idx")
        ]

    def __str__(self):
        return f"Vote on a post \"{self.post}\" by {self.user.username}"


class CommentVote(models.Model):
    user = models.ForeignKey('users.LitterUser', on_delete=models.DO_NOTHING)
    comment = models.ForeignKey(Comment, related_name='commentvote',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'comment'],
                                    name="Unique comment vote.")
            ]
        indexes = [
            models.Index(fields=['user', 'comment'],
                         name="commentvote_user_comment_idx")
        ]

    def __str__(self):
        return f"Vote on a post \"{self.comment}\" by {self.user.username}"
