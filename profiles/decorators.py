from functools import wraps

from django.shortcuts import get_object_or_404, redirect

from users.models import LitterUser


def owner_only():
    def decorator(function):
        @wraps(function)
        def _wrapped_view(request, *args, **kwargs):
            usertag = kwargs.get('usertag')
            if request.user != get_object_or_404(LitterUser, usertag=usertag):
                return redirect('core:feed')

            return function(request, *args, **kwargs)
        return _wrapped_view
    return decorator
