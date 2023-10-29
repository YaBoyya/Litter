from django.db import models
from django.db.models.query import QuerySet


class VotingManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().annotate(
            vote_count=models.Count('vote')
        )
