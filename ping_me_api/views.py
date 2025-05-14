from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView

from .settings import SIMPLE_JWT


class SetCookieMixin:
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):
            response.set_cookie(SIMPLE_JWT["REFRESH_TOKEN_NAME"], response.data["refresh"], max_age=SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"], httponly=True, samesite=SIMPLE_JWT["JWT_COOKIE_SAMESITE"])
        
        if response.data.get("access"):
            response.set_cookie(SIMPLE_JWT["ACCESS_TOKEN_NAME"], response.data["access"], max_age=SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"], httponly=True, samesite=SIMPLE_JWT["JWT_COOKIE_SAMESITE"])
        return super().finalize_response(request, response, *args, **kwargs)
    
class CookieTokenObtainPairView(SetCookieMixin, TokenObtainPairView):
    pass