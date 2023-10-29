from django.db import models
from pygments.lexers import get_all_lexers

# from users.models import LitterUser

# TODO setup get_text_lazy
LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0])for item in LEXERS])


class Post(models.Model):
    # user = models.ForeignKey(LitterUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=500, null=True, blank=True)
    language = models.CharField(choices=LANGUAGE_CHOICES)
    DIFFICULTY = [
        ('E', 'Easy'),
        ('M', 'Medium'),
        ('H', 'Hard'),
    ]
    difficulty = models.CharField(choices=DIFFICULTY, null=True)
    views = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    # user = models.ForeignKey(LitterUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)


class PostVote(models.Model):
    # user = models.ForeignKey(LitterUser, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class CommentVote(models.Model):
    # user = models.ForeignKey(LitterUser, on_delete=models.DO_NOTHING)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
