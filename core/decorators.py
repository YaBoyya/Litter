from functools import wraps

from django.shortcuts import redirect
from django.contrib import messages


def author_only(obj, message="You are not the owner.",
                redirect_url='core:feed'):
    def decorator(function):
        @wraps(function)
        def _wrapped_view(request, *args, **kwargs):
            pk = kwargs.get('pk')
            if request.user == obj.objects.get(id=pk).user:
                return function(request, *args, **kwargs)
            else:
                messages.info(request, message)
                return redirect(redirect_url)
        return _wrapped_view
    return decorator
