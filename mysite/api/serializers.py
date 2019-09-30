from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import Images
from rest_framework import serializers, viewsets, status, mixins, permissions

class SignupUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', "username", 'password',)
        extra_kwargs = {"password" : {"write_only" : True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"], password=validated_data["password"]
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")

class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")

class ImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = '__all__'