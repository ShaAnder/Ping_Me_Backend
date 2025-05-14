from django.middleware.csrf import CsrfViewMiddleware


class CustomCsrfMiddleware(CsrfViewMiddleware):
    def process_view(self, request, callback, callback_args, callback_kwargs):
        if request.path.startswith('/api/'):
            return self._accept(request)
        return super().process_view(request, callback, callback_args, callback_kwargs)