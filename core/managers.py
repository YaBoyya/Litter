from django.db import models
from django.db.models.query import QuerySet


class PostManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().annotate(
            comment_count=models.Count('comment', distinct=True)
        )
