from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from chats.models import ChatGroup, ChatMessage
from chats.serializers import ChatGroupSerializer, ChatMessageSerializer

User = get_user_model()


class ChatGroupViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )
    serializer_class = ChatGroupSerializer
    queryset = ChatGroup.objects.all()

    def perform_create(self, serializer):
        instance = serializer.save()
        # Add created user to the group by default
        instance.participants.add(self.request.user)

    @action(methods=["POST"], detail=True, url_path="add-participant")
    def add_participant(self, request, pk=None):
        chat_group = get_object_or_404(ChatGroup, pk=pk)  # type: ChatGroup
        user = get_object_or_404(User, pk=request.data.get("username", ""))
        chat_group.participants.add(user)
        return Response(ChatGroupSerializer(chat_group).data)


class ChatMessageViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )
    serializer_class = ChatMessageSerializer
    queryset = ChatMessage.objects.all()
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter
    )
    pagination_class = LimitOffsetPagination
    filterset_fields = ("group", "receiver")
    ordering_fields = ("timestamp", )

    def perform_create(self, serializer):
        # Make authenticated user as sender
        serializer.save(sender=self.request.user)

    @action(methods=["GET"], detail=False, url_path="direct-chats")
    def direct_chats(self):
        pass

    @action(methods=["GET"], detail=False, url_path="group-chats")
    def direct_chats(self):
        pass
