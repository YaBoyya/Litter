from django.db import models
from django.db.models.query import QuerySet


class PostManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().annotate(
            vote_count=models.Count('vote', distinct=True),
            comment_count=models.Count('comment', distinct=True)
        )


class CommentManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().annotate(
            vote_count=models.Count('vote')
        )
