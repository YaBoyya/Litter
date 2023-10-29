# from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.validators import UnicodeUsernameValidator
# from django.db import models
# from django.utils.translation import gettext_lazy as _


# # Create your models here.
# # TODO unique usertag and non unique username,
# # email login and registration

# # app is not connected for now
# class LitterUser(AbstractUser):
#     usertag = models.CharField(
#         _("username"),
#         max_length=150
#     )
#     username_validator = UnicodeUsernameValidator()
#     username = models.CharField(
#         _("usertag"),
#         max_length=150,
#         unique=True,
#         help_text=_(
#             "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
#         ),
#         validators=[username_validator],
#         error_messages={
#             "unique": _("A user with that usertag already exists."),
#         },
#     )
#     bio = models.TextField(max_lenght=200, null=True, blank=True)
#     # picture = models.ImageField()

#     USERNAME_FIELD = "usertag"
