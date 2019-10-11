from django.utils.deprecation import MiddlewareMixin
from django.middleware.csrf import get_token


class Mymiddleware(MiddlewareMixin):
    def process_request(self, request):
        get_token(request)