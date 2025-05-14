from rest_framework_simplejwt.authentication import JWTAuthentication
from ping_me_api.settings import SIMPLE_JWT


class JWTCookieAuthentication(JWTAuthentication):
    def authenticate(self, request):
        raw_token= request.COOKIE.get(SIMPLE_JWT["ACCESS_TOKEN_NAME"]) or None

        if raw_token is None:
            return None
        
        validate_token = self.get_validated_token(raw_token)
        return self.get_user(validate_token), validate_token