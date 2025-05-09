from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from .models import ConversationModel
from .schemas import list_message_docs
from .serializers import MessageSerializer


class MessageViewSet(viewsets.ViewSet):
    @list_message_docs
    def list(self, request):
        channel_id = request.query_params.get("channel_id")
        conversation = ConversationModel.objects.filter(channel_id=channel_id).first()
        if not conversation:
            return Response([])
        message = conversation.messages.all()

        serializer = MessageSerializer(message, many=True)
        return Response(serializer.data)