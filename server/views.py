from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Server
from .serializers import ServerSerializer

# we're opting for building a viewset instead of building each endpoint out, then
# we will return the endpoint based on what parameters are passed. While doing an endpoint
# for every piece of data we want to return can work for larger projects it can become
# tedius...

class ServerListViewSet(viewsets.ViewSet):

  queryset = Server.objects.all()

  def list(self, request):
    category = request.query_params.get("category")
    qty = request.query_params.get("qty")
    by_user = request.query_params.get("by_user") == "true"
    mutual_with = request.query_params.get("mutual_with")
    by_serverid = request.query_params.get("by_serverid")

    if category:
      self.queryset = self.queryset.filter(category__name=category)

    if qty:
      self.queryset = self.queryset[: int(qty)]

    if by_user:
      user_id = request.user.id
      self.queryset = self.queryset.filter(members=user_id)

    # testing mutual servers
    if mutual_with:
      try:
          other_user_id = int(mutual_with)
          self.queryset = self.queryset.filter(
              members=request.user.id
          ).filter(
              members=other_user_id
          )
      except ValueError:
          return Response({"error": "Invalid mutual_with user ID"}, status=400)
      
    if by_serverid:
      try:
          self.queryset = self.queryset.filter(id=by_serverid)
          if not self.queryset.exists():
            raise ValidationError(detail=f"Server with id {by_serverid} not found")
      except ValueError:
        raise ValidationError(detail=f"Server with id {by_serverid} not found")

    serializer = ServerSerializer(self.queryset, many=True)
    return Response(serializer.data)
