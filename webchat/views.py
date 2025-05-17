from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from .models import ConversationModel, Messages
from .serializers import MessageSerializer


class IsSenderOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the sender of a message to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or obj.sender == request.user

class MessageViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated, IsSenderOrReadOnly]

    def list(self, request):
        channel_id = request.query_params.get("channel_id")
        conversation = ConversationModel.objects.filter(channel_id=channel_id).first()
        if conversation:
            messages = conversation.messages.all()
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)
        return Response([])

    def retrieve(self, request, pk=None):
        try:
            msg = Messages.objects.get(pk=pk)
        except Messages.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, msg)
        serializer = MessageSerializer(msg)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        try:
            msg = Messages.objects.get(pk=pk)
        except Messages.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, msg)
        serializer = MessageSerializer(msg, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        try:
            msg = Messages.objects.get(pk=pk)
        except Messages.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, msg)
        msg.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
