from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Notification(models.Model):
    recipient = models.ForeignKey('users.LitterUser', related_name='recipient',
                                  on_delete=models.CASCADE)
    sender = models.ForeignKey('users.LitterUser', related_name='sender',
                               on_delete=models.DO_NOTHING)
    ACTIVITY_CHOICES = (
            (COMMENT := 'comment', 'has commented on your post.'),
            (FOLLOW := 'follow', 'has followed you.')
        )
    activity_type = models.CharField(
        _('Activity Type'),
        choices=ACTIVITY_CHOICES
    )
    OBJECT_CHOICES = [
            (COMMENT := 'comment', 'Comment'),
            (FOLLOW := 'follow', 'Follow')
        ]
    object_type = models.CharField(
        _('Object type'),
        choices=OBJECT_CHOICES
    )
    object_url = models.URLField(_('Object URL'))
    time_sent = models.DateTimeField(_('Time sent'),
                                     auto_now_add=timezone.now())
    is_unread = models.BooleanField(_('Is unread'), default=True)

    def __str__(self):
        return f"@{ self.sender.usertag } { self.get_activity_type_display() }"

    class Meta:
        ordering = ['-time_sent']
