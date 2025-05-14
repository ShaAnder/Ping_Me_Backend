from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from ping_me_api.settings import SIMPLE_JWT

from .models import Account
from .schemas import account_list_docs
from .serializers import AccountSerializer


class AccountViewSet(viewsets.ViewSet):
    queryset = Account.objects.all()
    permission_classes = [IsAuthenticated]

    @account_list_docs
    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get('user')
        if user_id:
            account = get_object_or_404(Account, owner__id=user_id)
            serializer = AccountSerializer(account)
            return Response(serializer.data)
        return Response({"detail": "User ID is required."}, status=400)

class SetCookieMixin:
    def finalize_response(self, request, response, *args, **kwargs):
        # If the view returned a refresh token, set it in a cookie:
        if "refresh" in response.data:
            response.set_cookie(
                SIMPLE_JWT["REFRESH_TOKEN_NAME"],
                response.data["refresh"],
                max_age=SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                httponly=True,
                samesite=SIMPLE_JWT["JWT_COOKIE_SAMESITE"],
            )
        # If the view returned an access token, set it in a cookie:
        if "access" in response.data:
            response.set_cookie(
                SIMPLE_JWT["ACCESS_TOKEN_NAME"],
                response.data["access"],
                max_age=SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                httponly=True,
                samesite=SIMPLE_JWT["JWT_COOKIE_SAMESITE"],
            )


        return super().finalize_response(request, response, *args, **kwargs)
    
class CookieTokenObtainPairView(SetCookieMixin, TokenObtainPairView):
    pass

class CookieTokenRefreshView(SetCookieMixin, TokenRefreshView):
    pass