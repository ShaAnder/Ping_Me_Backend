from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from .serializers import ChannelSerializer, ServerSerializer

server_list_docs = extend_schema(
  responses=ServerSerializer(many=True),
  parameters=[
    OpenApiParameter(
      name="category",
      type=OpenApiTypes.STR,
      location=OpenApiParameter.QUERY,
      description="Category of servers to retrieve",
    )
  ]
)