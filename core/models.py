from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import VotingManager


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

    objects = VotingManager()

    def __str__(self):
        return f'{self.text[:50]}...' if len(self.title) > 50 else self.title


class Comment(models.Model):
    user = models.ForeignKey('users.LitterUser', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(_("Text"), max_length=200)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    was_edited = models.BooleanField(_('Was edited'), default=False)

    objects = VotingManager()

    def __str__(self):
        return f'{self.text[:50]}...' if len(self.text) > 50 else self.text


class PostVote(models.Model):
    user = models.ForeignKey('users.LitterUser', on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Post, related_name='vote',
                             on_delete=models.CASCADE)
    created = models.DateTimeField(_("Created"), auto_now_add=True)


class CommentVote(models.Model):
    user = models.ForeignKey('users.LitterUser', on_delete=models.DO_NOTHING)
    comment = models.ForeignKey(Comment, related_name='vote',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
