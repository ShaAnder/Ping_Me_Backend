"""
OpenAPI schema extension for the message list endpoint.

This module provides documentation for the message list API endpoint,
including the response schema and query parameters for use with drf_spectacular.
"""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from .serializers import MessageSerializer

#: Schema extension for the message list endpoint.
#:
#: Adds response documentation and a query parameter for filtering messages by channel.
list_message_docs = extend_schema(
    responses=MessageSerializer(many=True),
    parameters=[
        OpenApiParameter(
            name="channel_id",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="ID of the channel",
        )
    ],
)
