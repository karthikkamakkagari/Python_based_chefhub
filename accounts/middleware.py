from django.utils import translation

class UserLanguageMiddleware:
    """
    Sets the user's preferred language for the session.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            language = user.preferred_language
            translation.activate(language)
            request.LANGUAGE_CODE = language
        response = self.get_response(request)
        return response
