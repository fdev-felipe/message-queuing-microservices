# encoding: utf-8

from rest_framework import serializers
from .models import UserRequestHistory, User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'username','is_superuser']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('username')

        return representation

class UserRequestStockSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserRequestHistory
        fields = ['date', 'name', 'symbol', 'open', 'high', 'low', 'close', 'user']
        extra_kwargs = {
            'id': {'write_only': True},
            'user': {'write_only': True}
        }


    def validate(self, data):
        data['symbol'] = data['symbol'].lower()
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('date')
        representation['symbol'] = representation['symbol'].upper()

        return representation


class UserRequestHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = UserRequestHistory
        fields = ['date', 'name', 'symbol', 'open', 'high', 'low', 'close', 'user']
        extra_kwargs = {
            'id': {'write_only': True},
            'user': {'write_only': True}
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['symbol'] = representation['symbol'].upper()

        return representation


class UserRequestStatsSerializer(serializers.ModelSerializer):
    stock = serializers.CharField(source='symbol')
    times_requested = serializers.IntegerField(label='times_requested', read_only=True)

    class Meta:
        model = UserRequestHistory
        fields = ['stock','times_requested']


    def to_representation(self, instance):
        representation = super().to_representation(instance)

        return representation