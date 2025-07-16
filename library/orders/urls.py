from django.urls import path
from orders.views import (CheckoutView, OrderConfirmationView, OrderDetailView)

urlpatterns = [
    path("<int:pk>", OrderDetailView.as_view(), name="order-detail"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path(
        "confirmation/<int:order_id>/",
        OrderConfirmationView.as_view(),
        name="order-confirmation",
    ),
]
