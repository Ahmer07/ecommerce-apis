from rest_framework import serializers

from .models import Order, Product
from users.serializers import ReadUserSerializer


class ProductSerializer(serializers.ModelSerializer):   

    class Meta:
        model = Product
        fields = ["name"]


class ReadOrderSerializer(serializers.ModelSerializer):   
    product = ProductSerializer()
    customer = ReadUserSerializer()

    class Meta:
        model = Order
        fields = '__all__'


class WriteOrderSerializer(serializers.ModelSerializer):   

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        validated_data['customer'] = self.context["request"].user
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
