from books.models import Genre
from django.views.generic import ListView
from products.models import Product


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
