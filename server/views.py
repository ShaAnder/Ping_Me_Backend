from django.db.models import Count
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ping_me_api.permissions import IsOwnerOrReadOnly

from .models import Channel, Server, ServerCategory
from .serializers import (ChannelSerializer, ServerCategorySerializer,
                          ServerSerializer)


class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        server = serializer.save(owner=self.request.user.account)
        server.members.add(self.request.user.account)
        Channel.objects.create(
            name="general",
            type=Channel.text,
            server=server,
            owner=self.request.user.account,  # <-- FIXED
            description="General text chat",
        )
        Channel.objects.create(
            name="vc gener",
            type=Channel.voice,
            server=server,
            owner=self.request.user.account,  # <-- FIXED
        )
        return server


    def get_queryset(self):
        queryset = Server.objects.all()
        request = self.request
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = request.query_params.get("by_user") == "true"
        mutual_with = request.query_params.get("mutual_with")
        by_serverid = request.query_params.get("by_serverid")
        with_num_members = request.query_params.get("with_num_members") == "true"

        if category:
            queryset = queryset.filter(category__name=category)
        if by_user and request.user.is_authenticated:
            queryset = queryset.filter(members=request.user.id)
        if mutual_with and request.user.is_authenticated:
            try:
                other_user_id = int(mutual_with)
                queryset = queryset.filter(members=request.user.id).filter(members=other_user_id)
            except ValueError:
                return queryset.none()
        if by_serverid:
            try:
                queryset = queryset.filter(id=by_serverid)
            except ValueError:
                return queryset.none()
        if with_num_members:
            queryset = queryset.annotate(num_members=Count("members"))
        if qty:
            try:
                queryset = queryset[: int(qty)]
            except ValueError:
                pass
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["num_members"] = self.request.query_params.get("with_num_members") == "true"
        return context

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_member(self, request, pk=None):
        server = self.get_object()
        account = request.user.account
        server.members.add(account)
        return Response({'status': 'member added'})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def remove_member(self, request, pk=None):
        server = self.get_object()
        account = request.user.account
        server.members.remove(account)
        return Response({'status': 'member removed'})


class ServerCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Provides list and retrieve for server categories.
    """
    serializer_class = ServerCategorySerializer
    queryset = ServerCategory.objects.all().order_by("name")

class ChannelViewSet(viewsets.ModelViewSet):
    """
    Provides full CRUD for channels.
    """
    serializer_class = ChannelSerializer
    queryset = Channel.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.account)
