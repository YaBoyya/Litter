from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Notification(models.Model):
    recipient = models.ForeignKey('users.LitterUser', related_name='recipient',
                                  on_delete=models.CASCADE)
    sender = models.ForeignKey('users.LitterUser', related_name='sender',
                               on_delete=models.DO_NOTHING)
    activity_type = models.CharField(
        _('Activity Type'),
        choices=[
            ('comment', 'comment on a post'),
            ('follow', 'new follow')
        ]
    )
    object_type = models.CharField(
        _('Object type'),
        choices=[
            ('comment', 'Comment'),
            ('follow', 'Follow')
        ]
    )
    object_url = models.URLField(_('Object URL'))
    time_sent = models.DateTimeField(_('Time sent'),
                                     auto_now_add=timezone.now())
    is_unread = models.BooleanField(_('Is unread'), default=True)

    def __str__(self):
        return f"{ self.sender } { self.activity_type }"
