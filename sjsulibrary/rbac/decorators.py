from django.http import HttpResponseForbidden
from functools import wraps

def roles_required(*role_names):
    """
    A decorator to restrict access to users with any of the specified roles.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                # Check if user has any of the roles
                if request.user.roles.filter(role_name__in=role_names).exists():
                    return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You do not have access to this page.")
        return _wrapped_view
    return decorator