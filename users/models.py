import os

from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _

from core.models import PathAndRename


class LitterUserManager(UserManager):
    def create_superuser(self, usertag, email, password, **extra_fields):
        extra_fields.update({'usertag': usertag})
        return super().create_superuser(usertag, email, password,
                                        **extra_fields)

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().annotate(
            notification_count=models.Count(
                'recipient',
                filter=models.Q(recipient__is_unread=True),
                distinct=True
                ),
            post_total=models.Count('post', distinct=True),
            comment_total=models.Count('comment', distinct=True),
        )


class LitterUser(AbstractUser):
    email = models.EmailField(_("email address"), error_messages={'unique': "This email has already been registered."})  # noqa
    username = models.CharField(
        _("username"),
        max_length=150
    )
    username_validator = UnicodeUsernameValidator()
    usertag = models.CharField(
        _("usertag"),
        max_length=150,
        unique=True,
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that usertag already exists."),
        },
    )
    following = models.ManyToManyField('self', related_name='followers',
                                       symmetrical=False)
    languages = models.ManyToManyField('core.Language')
    bio = models.TextField(_("Bio"), max_length=200, null=True, blank=True)
    picture = models.ImageField(default='default_pp.png',
                                upload_to=PathAndRename(
                                    'profile_pics/'))
    objects = LitterUserManager()
    USERNAME_FIELD = "usertag"

    class Meta:
        indexes = [
            models.Index(fields=['usertag'], name="litteruser_usertag_idx"),
            models.Index(fields=['id'], name="litteruser_id_idx")
        ]

    def delete(self, *args, **kwargs):
        if self.picture != 'default_pp.png':
            root = settings.MEDIA_ROOT
            relative_path = str(self.picture).replace("/", "\\")
            absolute_path = os.path.join(root, relative_path)
            os.remove(absolute_path)
        super().delete()

    def get_vote_list(self):
        return self.postvote_set.values_list('post_id', flat=True)
