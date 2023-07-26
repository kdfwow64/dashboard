from django.http import HttpResponse


class HealthCheckMiddleware:
    """
    This piece of middleware will return 'ok'/200 when '/health' endpoint is
    hit.  When using AWS ECS if there is nowhere a health check can be done
    ECS will restart the task as it thinks something is wrong.

    The motivation for this came from
    https://docs.djangoproject.com/en/3.2/topics/http/middleware/
    """

    def __init__(self, get_response):
        """
        The `get_response` callable provided by Django might be the actual view
        (if this is the last listed middleware) or it might be the next middleware
        in the chain. The current middleware doesn't need to know or care what
        exactly it is, just that it represents whatever comes next.

        This method, unlike `__call__`, is called once.

        :param get_response: callable
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Called once per request.

        :param request: the request
        """
        if request.path == "/health":
            return HttpResponse("ok")

        return self.get_response(request)
