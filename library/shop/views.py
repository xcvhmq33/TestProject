from books.models import Genre
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import DetailView, ListView
from shop.forms import OrderForm
from shop.models import CartItem, Order, OrderItem, Product


class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        queryset = super().get_queryset().select_related("book")
        category = self.request.GET.get("category")
        if category:
            queryset = queryset.filter(book__genre__name=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Genre.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.all()
        context["categories"] = Genre.objects.all()
        return context


class OrderDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Order
    template_name = "orders/order_detail.html"
    context_object_name = "order"

    def test_func(self):
        order = self.get_object()
        return order.user == self.request.user


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


class CheckoutView(LoginRequiredMixin, View):
    def get(self, request):
        cart_items = CartItem.objects.filter(user=request.user).select_related(
            "product", "product__book"
        )
        if not cart_items.exists():
            messages.info(request, "Ваша корзина пуста.")
            return redirect("cart-detail")

        form = OrderForm()
        context = {
            "form": form,
            "cart_items": cart_items,
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
