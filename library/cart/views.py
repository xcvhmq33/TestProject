from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from cart.models import CartItem, Product



class CartView(LoginRequiredMixin, View):
    def get(self, request):
        cart_items = CartItem.objects.select_related("product", "product__book").filter(
            user=request.user
        )
        item_prices = [item.product.price * item.quantity for item in cart_items]
        total_price = sum(item_prices)
        context = {
            "cart_items": cart_items,
            "item_prices": item_prices,
            "total_price": total_price,
        }
        return render(request, "cart/cart.html", context)


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        if product.stock <= 0:
            messages.error(
                request, f'Товар "{product.book.title}" закончился на складе.'
            )
            return redirect("product-list")

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user, product=product, defaults={"quantity": 1}
        )

        if not created:
            if cart_item.quantity < product.stock:
                cart_item.quantity += 1
                cart_item.save()
                messages.success(
                    request, f'Добавлено ещё один экземпляр "{product.book.title}".'
                )
            else:
                messages.info(
                    request, f'Больше экземпляров "{product.book.title}" нет в наличии.'
                )
        else:
            messages.success(
                request, f'Товар "{product.book.title}" добавлен в корзину.'
            )

        return redirect("product-list")


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, item_id, *args, **kwargs):
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
        cart_item.delete()
        return redirect("cart")
