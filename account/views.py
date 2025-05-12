from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Account
from .serializers import AccountSerializer


class AccountViewSet(viewsets.ViewSet):
    queryset = Account

    @extend_schema(responses=AccountSerializer)
    def list(self, request):
        serializer = AccountSerializer(self.queryset)
        return Response(serializer.data)