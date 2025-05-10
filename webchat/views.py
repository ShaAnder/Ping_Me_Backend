from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ConversationModel
from .schemas import list_message_docs
from .serializers import MessageSerializer


class MessageViewSet(viewsets.ViewSet):
    @list_message_docs
    def list(self, request):
        channel_id = request.query_params.get("channel_id")
        try:
            conversation = ConversationModel.objects.filter(channel_id=channel_id).first()
            message = conversation.messages.all()
            serializer = MessageSerializer(message, many=True)
            return Response(serializer.data)
        except ConversationModel.DoesNotExist:
            return Response([])
        

# class LastChannelViewSet(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]

#     # GET /api/servers/{server_id}/last-channel/
#     def list(self, request, server_pk=None):
#         last = LastChannel.objects.filter(user=request.user, server_id=server_pk).first()
#         return Response({"channel_id": last.channel_id if last else None})

#     # POST /api/servers/{server_id}/last-channel/  { "channel_id": "abc123" }
#     def create(self, request, server_pk=None):
#         cid = request.data.get("channel_id")
#         obj, _ = LastChannel.objects.update_or_create(
#             user=request.user,
#             server_id=server_pk,
#             defaults={"channel_id": cid},
#         )
#         return Response({"channel_id": obj.channel_id}, status=status.HTTP_201_CREATED)