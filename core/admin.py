from django.contrib import admin

from . import models


admin.site.register(models.Language)
admin.site.register(models.Post)
admin.site.register(models.PostVote)
admin.site.register(models.Comment)
admin.site.register(models.CommentVote)
