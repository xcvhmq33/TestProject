from django.urls import path
from cart.views import (AddToCartView, CartView, RemoveFromCartView)

urlpatterns = [
    path("add/<int:product_id>/", AddToCartView.as_view(), name="add-to-cart"),
    path(
        "remove/<int:item_id>/",
        RemoveFromCartView.as_view(),
        name="remove-from-cart",
    ),
    path("", CartView.as_view(), name="cart"),
]
