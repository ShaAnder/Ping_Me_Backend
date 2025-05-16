from django.db.models import Count
from rest_framework import permissions, viewsets

from .models import Channel, Server, ServerCategory
from .serializers import (ChannelSerializer, ServerCategorySerializer,
                          ServerSerializer)


class ServerViewSet(viewsets.ModelViewSet):
    """
    Provides list, create, retrieve, update, partial_update, and destroy for servers.
    """
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """
        Set the owner to the current user and auto-create default channels.
        """
        server = serializer.save(owner=self.request.user)
        # Create default channels
        Channel.objects.create(
            name="general",
            type=Channel.text,
            server=server,
            owner=self.request.user,
            description="General text chat",
        )
        Channel.objects.create(
            name="vc gener",
            type=Channel.voice,
            server=server,
            owner=self.request.user,
        )
        return server

    def get_queryset(self):
        """
        Optionally filter by category, user, etc., based on query params.
        """
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

    # Optionally, override get_serializer_context to pass extra context
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["num_members"] = self.request.query_params.get("with_num_members") == "true"
        return context

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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
