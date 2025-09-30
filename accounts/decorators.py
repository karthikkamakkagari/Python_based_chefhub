from django.shortcuts import redirect
from functools import wraps

def token_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.account_type == 'SUPREM' or request.user.token > 0:
            return view_func(request, *args, **kwargs)
        return redirect('dashboard')
    return _wrapped_view
