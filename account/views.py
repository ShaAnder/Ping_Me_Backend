from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from ping_me_api.settings import SIMPLE_JWT
from ping_me_api.utils import generate_token, verify_token

from .models import Account
from .schemas import account_list_docs
from .serializers import AccountRegistrationSerializer, AccountSerializer


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


class AccountViewSet(viewsets.ViewSet):
    queryset = User.objects.all()

    # Registration endpoint: /api/account/register/
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = AccountRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = generate_token(user)
            verify_url = f"{request.scheme}://{request.get_host()}/verify-email/?token={token}"
            send_mail(
                'Verify your email',
                f"Hi {user.username}, click to verify: {verify_url}",
                'pingmepp5@gmail.com',
                [user.email],
                fail_silently=False,
            )
            return Response({'message': 'Registration successful. Check your email.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Email verification endpoint: /api/account/verify_email/
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def verify_email(self, request):
        token = request.GET.get('token')
        user_pk = verify_token(token)
        if user_pk:
            try:
                user = User.objects.get(pk=user_pk)
                user.is_active = True
                user.save()
                return Response({'message': 'Email verified. You can now log in.'})
            except User.DoesNotExist:
                pass
        return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

    # Optionally, add profile retrieval (requires auth)
    def retrieve(self, request, pk=None):
        user = self.get_object()
        serializer = AccountSerializer(user)
        return Response(serializer.data)
