from functools import wraps
from django.http import JsonResponse

def del_session(request):
    request.session.pop("solution_id", None)
    request.session.pop("user", None)
    request.session.pop("username", None)
    request.session.pop("user_id", None)
    return JsonResponse({"status": "session_expired"})


def login_required(func):
    @wraps(func)
    def get_session(request, *args, **kwargs):
        if ("soln" == request.path.rstrip("/").rsplit("/", 1)[-1]) or ("activeTenant" == request.path.rstrip("/").rsplit("/", 1)[-1]):
            if request and request.session.keys() and [True if key in ["user_id", "user","username"] else False for key in list(request.session.keys())]:
                result = func(request, *args, **kwargs)
            else:
               return del_session(request)
        elif request.session.keys() and [True if key in ["user_id", "solution_id", "user","username"] else False for key in list(request.session.keys())]:
            result = func(request, *args, **kwargs)
        else:
            return del_session(request)
        return result
    return get_session