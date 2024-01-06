from django.apps import apps
from django.db import models
from django.db.models import Exists, OuterRef, Prefetch
from django.db.models.query import QuerySet


class CommentManager(models.Manager):
    def get_voted(self, user=None) -> QuerySet:
        comment_vote = apps.get_model('core', 'CommentVote')
        return super().get_queryset().annotate(
            has_voted=Exists(comment_vote.objects.filter(
                user=user,
                comment_id=OuterRef('pk'))
            )
        )


class PostManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().annotate(
            comment_count=models.Count('comment', distinct=True)
        )

    def get_voted(self, user=None) -> QuerySet:
        post_vote = apps.get_model('core', 'PostVote')
        return self.get_queryset().annotate(
            comment_count=models.Count('comment', distinct=True),
            has_voted=Exists(post_vote.objects.filter(
                user=user,
                post_id=OuterRef('pk'))
            )
        )

    def get_sorted_feed(self, user, sort):
        qs = self.get_voted(user).select_related(
                'user').prefetch_related(Prefetch('languages'))

        if sort == 'new':
            return qs.order_by('-created')
        elif sort == 'hot':
            return qs.order_by(
                '-created',
                '-total_votes',
                '-comment_count',
                )
        elif sort == 'top':
            return qs.order_by('-total_votes')
        return qs
