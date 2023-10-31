from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class LitterUserManager(UserManager):
    def create_superuser(self, usertag, email, password, **extra_fields):
        extra_fields.update({'usertag': usertag})
        return super().create_superuser(usertag, email, password,
                                        **extra_fields)


class LitterUser(AbstractUser):
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
    # TODO install Pillow and setup pfp
    # picture = models.ImageField()
    objects = LitterUserManager()
    USERNAME_FIELD = "usertag"
