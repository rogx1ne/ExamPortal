from functools import wraps

from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse


def role_required(required_role: str):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(f"{reverse('login')}?next={request.get_full_path()}")
            if getattr(request.user, "role", None) != required_role:
                return HttpResponseForbidden("You are not allowed to access this page.")
            return view_func(request, *args, **kwargs)

        return _wrapped

    return decorator


admin_required = role_required("ADMIN")
student_required = role_required("STUDENT")

