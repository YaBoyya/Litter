from django.db import models
from django.utils.translation import gettext_lazy as _
from pygments.lexers import get_all_lexers

from .managers import VotingManager
from users.models import LitterUser


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0])for item in LEXERS])


class Post(models.Model):
    user = models.ForeignKey(LitterUser, on_delete=models.CASCADE)
    title = models.CharField(_("Title"), max_length=100)
    text = models.TextField(_("Description"), max_length=500, null=True,
                            blank=True)
    language = models.CharField(_("Programming language"),
                                choices=LANGUAGE_CHOICES)
    DIFFICULTY = [
        ('E', 'Easy'),
        ('M', 'Medium'),
        ('H', 'Hard'),
    ]
    difficulty = models.CharField(_("Difficulty"), choices=DIFFICULTY,
                                  null=True)
    views = models.IntegerField(_("Views"), default=0)
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    objects = VotingManager()

    def __str__(self):
        return f'{self.text[:50]}...' if len(self.title) > 50 else self.title


class Comment(models.Model):
    user = models.ForeignKey(LitterUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(_("Text"), max_length=200)
    created = models.DateTimeField(_("Created"), auto_now_add=True)

    objects = VotingManager()

    def __str__(self):
        return f'{self.text[:50]}...' if len(self.text) > 50 else self.text


class PostVote(models.Model):
    user = models.ForeignKey(LitterUser, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Post, related_name='vote',
                             on_delete=models.CASCADE)
    created = models.DateTimeField(_("Created"), auto_now_add=True)


class CommentVote(models.Model):
    user = models.ForeignKey(LitterUser, on_delete=models.DO_NOTHING)
    comment = models.ForeignKey(Comment, related_name='vote',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
