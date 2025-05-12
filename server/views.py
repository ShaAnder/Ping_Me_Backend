from django.db.models import Count
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import filters, viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Server, ServerCategory
from .schema import server_list_docs
from .serializers import ServerCategorySerializer, ServerSerializer

# we're opting for building a viewset instead of building each endpoint out, then
# we will return the endpoint based on what parameters are passed. While doing an endpoint
# for every piece of data we want to return can work for larger projects it can become
# tedius...


class ServerListViewSet(viewsets.ViewSet):

    queryset = Server.objects.all()
    # permission_classes = [IsAuthenticated]

    @server_list_docs
    def list(self, request):
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = request.query_params.get("by_user") == "true"
        mutual_with = request.query_params.get("mutual_with")
        by_serverid = request.query_params.get("by_serverid")
        with_num_members = request.query_params.get("with_num_members") == "true"

        if by_user and not request.user.is_authenticated:
            raise AuthenticationFailed()

        if category:
            self.queryset = self.queryset.filter(category__name=category)

        if by_user:
            user_id = request.user.id
            self.queryset = self.queryset.filter(members=user_id)

        if qty:
            self.queryset = self.queryset[: int(qty)]

        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("members"))

        # testing mutual servers
        if mutual_with:
            try:
                other_user_id = int(mutual_with)
                self.queryset = self.queryset.filter(members=request.user.id).filter(
                    members=other_user_id
                )
            except ValueError:
                return Response({"error": "Invalid mutual_with user ID"}, status=400)

        if by_serverid:
            try:
                self.queryset = self.queryset.filter(id=by_serverid)
                if not self.queryset.exists():
                    raise ValidationError(
                        detail=f"Server with id {by_serverid} not found"
                    )
            except ValueError:
                raise ValidationError(detail=f"Server with id {by_serverid} not found")

        serializer = ServerSerializer(
            self.queryset, many=True, context={"num_members": with_num_members}
        )
        return Response(serializer.data)


class ServerCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list:
        Return all categories.

    retrieve:
        Return a single category by ID.
    """
    serializer_class = ServerCategorySerializer
    queryset = ServerCategory.objects.all().order_by("name")

    @extend_schema(responses=ServerCategorySerializer)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
