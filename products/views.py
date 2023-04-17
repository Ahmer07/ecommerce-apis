from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView , GenericAPIView

from users.permissions import IsSuperAdmin, IsCustomer, IsOwner
from .models import Order, Product
from .serializers import ProductSerializer, ReadOrderSerializer, WriteOrderSerializer


class ProductsView(ListCreateAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    serializer_class = ProductSerializer


class OrdersView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsCustomer|IsSuperAdmin]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return WriteOrderSerializer
        else:
            return ReadOrderSerializer

    def get_queryset(self):
        if self.request.user.role == "super_admin":
            return Order.objects.all()
        return Order.objects.filter(customer=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class SpecificOrderView(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = ReadOrderSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin|IsOwner]
    http_method_names = ["patch", "delete", "get"]


class GetOrdersByEmailView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def post(self, request):
        emails = request.data["emails"]
        orders = Order.objects.filter(customer__email__in=emails)
        serialized_orders = ReadOrderSerializer(orders, many=True)
        return Response(serialized_orders.data, 200)
