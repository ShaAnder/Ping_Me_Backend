from django.shortcuts import render
from rest_framework import viewsets
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
    if category:
      self.queryset = self.queryset.filter(category__name=category)
    serializer = ServerSerializer(self.queryset, many=True)
    return Response(serializer.data)
