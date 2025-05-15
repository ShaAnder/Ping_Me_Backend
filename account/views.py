import os

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from dotenv import load_dotenv
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from ping_me_api.utils import generate_token, verify_token

from .serializers import (AccountRegistrationSerializer, AccountSerializer,
                          PasswordResetConfirmSerializer,
                          PasswordResetRequestSerializer,
                          ResendVerificationSerializer)

load_dotenv()

class AccountViewSet(viewsets.ViewSet):

    # Registration endpoint: /api/account/register/
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = AccountRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate uidb64 and token
            uidb64, token = generate_token(user)
            # Build verification URL
            # Build verification URL (as before)
            verify_url = f"https://ping-me-pp5-backend-6aaeef173b97.herokuapp.com/api/account/verify_email/?uid={uidb64}&token={token}"
            logo_url = "http://localhost:8000/static/admin/img/pingMe.png"
            # Render HTML email template
            html_message = render_to_string(
                'emails/verify_email.html',
                {
                    'user': user,
                    'verification_url': verify_url,
                    'logo_url': logo_url,
                }
            )
            plain_message = f"Hi {user.username}, click to verify: {verify_url}"

            send_mail(
                'Verify your email',
                plain_message,  # Fallback for clients that don't support HTML
                'pingmepp5@gmail.com',
                [user.email],
                fail_silently=False,
                html_message=html_message,
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
            # Use environment variable to determine redirect URL
            if os.environ.get("DEV"):
                redirect_url = os.environ.get("CLIENT_ORIGIN_DEV")
            else:
                redirect_url = os.environ.get("CLIENT_ORIGIN")
            return HttpResponseRedirect(redirect_url)
        return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
    
    #Resend the email
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

    # Forgot password endpoint: /api/account/password_reset/
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def password_reset(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            if os.environ.get("DEV"):
                frontend_origin = os.environ.get("CLIENT_ORIGIN_DEV")
            else:
                frontend_origin = os.environ.get("CLIENT_ORIGIN")

            reset_url = f"{frontend_origin}/app/reset/{uid}/{token}"
            logo_url = "http://localhost:8000/static/admin/img/pingMe.png"
            html_message = render_to_string(
                'emails/reset_password.html',
                {
                    'user': user,
                    'reset_url': reset_url,
                    'logo_url': logo_url,
                }
            )
            plain_message = f"Hi {user.username}, click to reset your password: {reset_url}"
            send_mail(
                "Reset your PingMe password",
                plain_message,
                'pingmepp5@gmail.com',
                [user.email],
                fail_silently=False,
                html_message=html_message,
            )
        except User.DoesNotExist:
            pass
        return Response({'message': 'If this email is registered, a password reset link has been sent.'})

    # Reset confirmation endpoint: /api/account/password_reset_confirm/
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def password_reset_confirm(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uid = serializer.validated_data['uid']
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password1']
        try:
            uid_int = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid_int)
            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                if os.environ.get("DEV"):
                    redirect_url = os.environ.get("CLIENT_ORIGIN_DEV")
                else:
                    redirect_url = os.environ.get("CLIENT_ORIGIN")
                return Response({
                    'message': 'Password has been reset successfully.',
                    'redirect_url': redirect_url + '/login'
                })
            else:
                return Response({'error': 'Invalid or expired token.'}, status=400)
        except Exception:
            return Response({'error': 'Invalid request.'}, status=400)

#--------------------------#
###### user endpoints ######

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        account = request.user.account
        serializer = AccountSerializer(account)
        return Response(serializer.data)
    
    @action(detail=False, methods=['patch'], permission_classes=[IsAuthenticated])
    def edit_me(self, request):
        account = request.user.account
        serializer = AccountSerializer(account, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)