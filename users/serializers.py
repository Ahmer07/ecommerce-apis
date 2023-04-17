from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core import exceptions
from django.contrib.auth.hashers import make_password

from .models import User
from .exceptions import PrivilegeException


class WriteUserSerializer(serializers.ModelSerializer):   

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'password' : {'write_only' : True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = self.Meta.model(**validated_data)
        instance.set_password(password)
        instance.save()
        return instance

    def partial_update(self, instance, validated_data):
        if instance.is_deleted:
            raise PrivilegeException("Deleted user details can't be updated")
        if validated_data.get('email'):
            validated_data.pop('email')
        if validated_data.get('password'):
            instance.password = make_password(validated_data.get('password'))
        if self.context["request"].user.role != "customer":
            if validated_data.get('role'):
                instance.role = validated_data.get('role')
        instance.save()
        return instance


class ReadUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id' ,'first_name' , 'last_name', 'email' , "role" , 'password']


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user or user.is_deleted:
                msg = 'incorrect email or password'
                raise exceptions.ValidationError(msg)
            attrs['user'] = user
            return attrs
        else:
            msg = 'Must include "email" and "password"'
            raise exceptions.ValidationError(msg)
        
    class Meta:
        model = User
        fields = ['email' , 'passowrd']


class UsersEmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email']
