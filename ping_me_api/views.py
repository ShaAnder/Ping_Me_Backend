from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings

# Example SIMPLE_JWT config for reference
SIMPLE_JWT = getattr(settings, "SIMPLE_JWT", {})
ACCESS_TOKEN_NAME = SIMPLE_JWT.get("ACCESS_TOKEN_NAME", "access_token")
REFRESH_TOKEN_NAME = SIMPLE_JWT.get("REFRESH_TOKEN_NAME", "refresh_token")
ACCESS_TOKEN_LIFETIME = int(SIMPLE_JWT.get("ACCESS_TOKEN_LIFETIME", 300))  # seconds
REFRESH_TOKEN_LIFETIME = int(SIMPLE_JWT.get("REFRESH_TOKEN_LIFETIME", 604800))  # seconds
JWT_COOKIE_SAMESITE = SIMPLE_JWT.get("JWT_COOKIE_SAMESITE", "Lax")
JWT_COOKIE_SECURE = SIMPLE_JWT.get("JWT_COOKIE_SECURE", True)
JWT_COOKIE_DOMAIN = SIMPLE_JWT.get("JWT_COOKIE_DOMAIN", ".herokuapp.com")  # or your domain

class SetCookieMixin:
    def finalize_response(self, request, response, *args, **kwargs):
        data = getattr(response, 'data', {})
        if data and data.get("refresh"):
            response.set_cookie(
                REFRESH_TOKEN_NAME,
                data["refresh"],
                max_age=REFRESH_TOKEN_LIFETIME,
                httponly=True,
                samesite=JWT_COOKIE_SAMESITE,
                secure=JWT_COOKIE_SECURE,
                domain=JWT_COOKIE_DOMAIN,
                path="/",  # so it's sent for all endpoints
            )
        if data and data.get("access"):
            response.set_cookie(
                ACCESS_TOKEN_NAME,
                data["access"],
                max_age=ACCESS_TOKEN_LIFETIME,
                httponly=True,
                samesite=JWT_COOKIE_SAMESITE,
                secure=JWT_COOKIE_SECURE,
                domain=JWT_COOKIE_DOMAIN,
                path="/",
            )
        return super().finalize_response(request, response, *args, **kwargs)

class CookieTokenObtainPairView(SetCookieMixin, TokenObtainPairView):
    """
    Custom token view that sets JWTs in HttpOnly cookies.
    """
    pass