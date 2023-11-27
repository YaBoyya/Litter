from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

#TODO: rename post_form with statement in post_edit.html and post-create.html
#TODO: Cleanup login-register form
