from django.db import models
from django.utils.translation import gettext_lazy as _


class ChatRoom(models.Model):
    # TODO change id to uuid4
    users = models.ManyToManyField('users.LitterUser')
    title = models.CharField(_("Title"), null=True)
    is_private = models.BooleanField(default=True)


class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, related_name="messages",
                                 on_delete=models.CASCADE)
    user = models.ForeignKey('users.LitterUser', on_delete=models.DO_NOTHING)
    text = models.CharField(_("Text"))
    sent = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
