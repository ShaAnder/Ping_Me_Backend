from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from ping_me_api import settings

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

class JWTSetCookieMixin:
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):
            response.set_cookie(
                settings.SIMPLE_JWT["REFRESH_TOKEN_NAME"],
                response.data["refresh"],
                max_age=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                httponly=True,
                samesite=settings.SIMPLE_JWT["JWT_COOKIE_SAMESITE"],
            )
        if response.data.get("access"):
            response.set_cookie(
                settings.SIMPLE_JWT["ACCESS_TOKEN_NAME"],
                response.data["access"],
                max_age=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                httponly=True,
                samesite=settings.SIMPLE_JWT["JWT_COOKIE_SAMESITE"],
            )

        response.data.pop("access", None)

        return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenObtainPairView(JWTSetCookieMixin, TokenObtainPairView):
    pass

class CookieTokenRefreshView(JWTSetCookieMixin, TokenRefreshView):
    def post(self, request, *args, **kwargs):
        # Extract refresh token from cookie
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['REFRESH_TOKEN_NAME'])
        if refresh_token:
            request.data['refresh'] = refresh_token
        return super().post(request, *args, **kwargs)