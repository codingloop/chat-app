from rest_framework import serializers

from users.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "avatar", "password")


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "avatar")
        read_only_fields = ("username", )
