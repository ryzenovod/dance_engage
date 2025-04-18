class NgrokSkipBrowserWarningMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Добавляем заголовок к ответу
        response['ngrok-skip-browser-warning'] = 'true'

        return response
