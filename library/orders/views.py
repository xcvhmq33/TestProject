from cart.models import CartItem
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import DetailView
from orders.forms import OrderForm
from orders.models import Order, OrderItem


class OrderDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Order
    template_name = "orders/order_detail.html"
    context_object_name = "order"

    def test_func(self):
        order = self.get_object()
        return order.user == self.request.user


class CheckoutView(LoginRequiredMixin, View):
    def get(self, request):
        cart_items = CartItem.objects.filter(user=request.user).select_related(
            "product", "product__book"
        )
        if not cart_items.exists():
            messages.info(request, "Ваша корзина пуста.")
            return redirect("cart-detail")

        form = OrderForm()
        total_price = sum(item.total_price for item in cart_items)
        context = {
            "form": form,
            "cart_items": cart_items,
            "total_price": total_price,
        }
        return render(request, "orders/checkout.html", context)

    def post(self, request):
        cart_items = CartItem.objects.filter(user=request.user).select_related(
            "product", "product__book"
        )
        if not cart_items.exists():
            messages.info(request, "Ваша корзина пуста.")
            return redirect("cart-detail")

        form = OrderForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.user = request.user
                order.save()

                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price,
                    )

                    item.product.stock = max(item.product.stock - item.quantity, 0)
                    item.product.save()

                cart_items.delete()

            messages.success(
                request, f"Спасибо за заказ, {order.full_name}! Ваш заказ принят."
            )
            return redirect("order-confirmation", order_id=order.id)
        else:
            context = {
                "form": form,
                "cart_items": cart_items,
            }
            return render(request, "orders/checkout.html", context)


class OrderConfirmationView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        context = {"order": order}
        return render(request, "orders/order_confirmation.html", context)
