from django.apps import apps
from django.utils import timezone
from django.db import models
from django.db.models import Exists, F, OuterRef, Prefetch
from django.db.models.expressions import Func
from django.db.models.query import QuerySet


class Epoch(Func):
    template = 'EXTRACT(epoch FROM %(expressions)s)::INTEGER'
    output_field = models.IntegerField()


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
            comment_count=models.Count('comment', distinct=True),
            popularity=(F('views')*F('total_votes')*F('comment_count')
                        / (1+Epoch(timezone.now()-F('created')))))

    def get_voted(self, user=None) -> QuerySet:
        post_vote = apps.get_model('core', 'PostVote')
        return self.get_queryset().annotate(
            comment_count=models.Count('comment', distinct=True),
            has_voted=Exists(post_vote.objects.filter(
                user=user,
                post_id=OuterRef('pk'))
            )
        )

    def get_sorted_feed(self, user=None, sort=None):
        qs = self.get_voted(user).select_related(
                'user').prefetch_related(Prefetch('languages'))

        if sort == 'new':
            return qs.order_by('-created')
        elif sort == 'hot':
            return qs.order_by('-popularity')
        elif sort == 'top':
            return qs.order_by('-total_votes')
        return qs
