from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Account
from .serializers import AccountSerializer


class AccountViewSet(viewsets.ViewSet):
    queryset = Account.objects.all()

    @extend_schema(responses=AccountSerializer)
    def list(self, request):


        user_id = request.query_params.get("user_id")
        queryset = self.queryset.filter(id=user_id)
        serializer = AccountSerializer(queryset)
        return Response(serializer.data)