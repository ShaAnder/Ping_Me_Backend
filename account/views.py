from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Account
from .schemas import account_list_docs
from .serializers import AccountSerializer#
from rest_framework.permissions import IsAuthenticated


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
