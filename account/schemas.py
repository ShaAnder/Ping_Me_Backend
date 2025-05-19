"""
OpenAPI schema extension for the account list endpoint.

This module defines the documentation for the account list API endpoint,
including response schema and query parameters for use with drf_spectacular.
"""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from .serializers import AccountSerializer

#: Schema extension for the account list endpoint.
#: 
#: Adds response documentation and a user query parameter for filtering by user ID.
account_list_docs = extend_schema(
    responses=AccountSerializer(many=True),
    parameters=[
        OpenApiParameter(
            name="user",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="User ID",
        ),
    ],
)
