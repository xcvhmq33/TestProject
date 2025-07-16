from django.urls import path
from shop.views import (AddToCartView, CartView, CheckoutView,
                        OrderConfirmationView, OrderDetailView,
                        ProductDetailView, ProductListView, RemoveFromCartView)

urlpatterns = [
    path("", ProductListView.as_view(), name="product-list"),
    path(
        "products/<int:product_id>/", ProductDetailView.as_view(), name="product-detail"
    ),
    path("add-to-cart/<int:product_id>/", AddToCartView.as_view(), name="add-to-cart"),
    path(
        "remove-from-cart/<int:item_id>/",
        RemoveFromCartView.as_view(),
        name="remove-from-cart",
    ),
    path("cart/", CartView.as_view(), name="cart"),
    path("orders/<int:pk>", OrderDetailView.as_view(), name="order-detail"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path(
        "order-confirmation/<int:order_id>/",
        OrderConfirmationView.as_view(),
        name="order-confirmation",
    ),
]
