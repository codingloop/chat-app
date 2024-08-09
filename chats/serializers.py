from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from chats.models import ChatGroup, ChatMessage
from users.serializers import BasicUserSerializer


class ChatGroupSerializer(serializers.ModelSerializer):
    participants = BasicUserSerializer(read_only=True, many=True)

    class Meta:
        model = ChatGroup
        fields = "__all__"


class ChatMessageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        group = validated_data.get("group")
        receiver = validated_data.get("receiver")

        # Make sure, for any message - group or receiver (only one of them) should be present
        if not group and not receiver:
            raise ValidationError("Either Group or receiver needs to be provided")

        if group and receiver:
            raise ValidationError("Only one of group or receiver can be present, provided both")

        return super().create(validated_data)

    def update(self, instance, validated_data):
        auth_user = self.context.get("request").user
        if instance.can_be_edited(auth_user):
            instance.content = validated_data.get('content')
            instance.edited = True
            instance.save()
            return instance
        raise ValidationError("Message cannot be edited")

    class Meta:
        model = ChatMessage
        fields = ('id', 'content', 'timestamp', 'edited', 'sender', 'group', 'receiver')
        read_only_fields = ('id', 'timestamp', 'edited', 'sender')
        extra_kwargs = {
            'group': {'write_only': True},
            'receiver': {'write_only': True}
        }


class ChatMessageListSerializer(serializers.ModelSerializer):
    # Do not use in Create/Edit/Delete views
    unread_count = serializers.SerializerMethodField()

    def get_unread_count(self, instance):
        user = self.context.get("user")
        # instance.[]
        pass

    class Meta:
        model = ChatMessage
        fields = ('id', 'content', 'timestamp', 'edited', 'sender', 'group', 'receiver',
                  'unread_count')
