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
            comment_total=models.Count('comment', distinct=True),
            followers_count=models.Count('followers', distinct=True),
            notification_count=models.Count(
                'recipient',
                filter=models.Q(recipient__is_unread=True),
                distinct=True
                ),
            post_total=models.Count('post', distinct=True),
        )


class LitterUser(AbstractUser):
    email = models.EmailField(_("email address"), error_messages={'unique': "This email has already been registered."})  # noqa
    languages = models.ManyToManyField('core.Language')
    username = models.CharField(
        _("username"),
        max_length=150
    )
    username_validator = UnicodeUsernameValidator()
    usertag = models.CharField(
        _("usertag"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."  # noqa
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that usertag already exists."),
        },
    )
    bio = models.TextField(_("Bio"), max_length=200, null=True, blank=True)
    picture = models.ImageField(default='default_pp.png',
                                upload_to=PathAndRename(
                                    'profile_pics/'))
    objects = LitterUserManager()
    USERNAME_FIELD = "usertag"

    def delete(self, *args, **kwargs):
        if self.picture != 'default_pp.png':
            root = settings.MEDIA_ROOT
            relative_path = str(self.picture).replace("/", "\\")
            absolute_path = os.path.join(root, relative_path)
            os.remove(absolute_path)
        super().delete()


class UserFollowing(models.Model):
    """
    If you filter user=request.user, you'll get what he is following
    and if you filter following_user=request.user, you'll get his followers
    """
    # is following
    user = models.ForeignKey(LitterUser, related_name="following",
                             on_delete=models.CASCADE)
    # is being followed
    followed_user = models.ForeignKey(LitterUser, related_name="followers",
                                      on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'followed_user'],
                                    name="unique_followers")
            ]

    def __str__(self):
        return f'{self.user.usertag} follows {self.followed_user.usertag}.'
