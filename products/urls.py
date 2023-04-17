from django.urls import path

from .views import ProductsView, OrdersView, SpecificOrderView, GetOrdersByEmailView

urlpatterns = [
    path('products/', ProductsView.as_view()),
    path('orders/', OrdersView.as_view()),
    path('orders/<uuid:pk>/', SpecificOrderView.as_view()),
    path('get_orders_by_email/', GetOrdersByEmailView.as_view()),
]
