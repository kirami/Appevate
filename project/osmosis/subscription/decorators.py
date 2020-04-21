from functools import wraps
from django.utils.decorators import available_attrs
from django.shortcuts import redirect
from django.contrib import messages

DEFAULT_MESSAGE = "You need to have an active subscription to continue. Let's collect your payment information."

"""
def is_user_subscribed(user):
    if hasattr(user, 'advertiser'):
        return user.advertiser.has_active_subscription()
    return False
"""


def requires_subscription(message=DEFAULT_MESSAGE, redirect_to=None):
    """Decorator to be applied to views, which ensures that a user has an active
    subscription
    """
    def decorator(view_func, message=message):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            # if user is subscribed we can proceed
            if is_user_subscribed(request.user):
                return view_func(request, *args, **kwargs)

            # otherwise redirect the user to `redirect_to` with a message
            path = request.get_full_path()
            messages.info(request, message)
            return redirect(redirect_to, {'next': path})

        return _wrapped_view
    return decorator
