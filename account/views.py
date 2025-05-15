from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ping_me_api.utils import generate_token, verify_token

from .serializers import (AccountRegistrationSerializer, AccountSerializer,
                          ResendVerificationSerializer)


class AccountViewSet(viewsets.ViewSet):
    queryset = User.objects.all()

    # Registration endpoint: /api/account/register/
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = AccountRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate uidb64 and token
            uidb64, token = generate_token(user)
            # Build verification URL
            verify_url = f"https://ping-me-pp5-backend-6aaeef173b97.herokuapp.com/api/account/verify_email/?uid={uidb64}&token={token}"
            
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
        uidb64 = request.GET.get('uid')
        token = request.GET.get('token')
        user = verify_token(uidb64, token)
        if user:
            user.is_active = True
            user.save()
            return Response({'message': 'Email verified. You can now log in.'})
        return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

    # Optionally, add profile retrieval (requires auth)
    def retrieve(self, request, pk=None):
        user = self.get_object()
        serializer = AccountSerializer(user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def resend_verification(self, request):
        serializer = ResendVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            if user.is_active:
                return Response({'message': 'Account already verified.'}, status=status.HTTP_200_OK)
            uidb64, token = generate_token(user)
            verify_url = (
                f"https://ping-me-pp5-backend-6aaeef173b97.herokuapp.com/api/account/verify_email/?uid={uidb64}&token={token}"
            )
            # Send the email
            send_mail(
                'Verify your email',
                f"Hi {user.username}, click to verify: {verify_url}",
                'pingmepp5@gmail.com',
                [user.email],
                fail_silently=False,
            )
            return Response({'message': 'Verification email resent.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            # For security, do not reveal if the email is not registered
            return Response({'message': 'If this email is registered and not yet verified, a verification email has been sent.'}, status=status.HTTP_200_OK)
