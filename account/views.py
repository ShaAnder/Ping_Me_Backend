from django.http import Http404
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from ping_me_api.permissions import IsOwnerOrReadOnly

from .models import Account
from .serializers import AccountSerializer


class AccountList(ListAPIView):
    """
    List all accounts.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class AccountDetail(RetrieveUpdateAPIView):
    """
    Retrieve or update a Account.
    Only the owner can update.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]