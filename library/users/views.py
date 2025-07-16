from books.models import Book
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from users.forms import ProfileUpdateForm, UserRegisterForm, UserUpdateForm

LIST_NAMES = ["planned", "reading", "dropped", "finished"]


class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save()
        username = form.cleaned_data["username"]
        messages.success(self.request, f"Добро пожаловать, {username}")
        return super().form_valid(form)


class RedirectToOwnProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return redirect("profile", username=request.user.username)


class ProfileView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        username = self.kwargs.get("username")
        return self.request.user.username.lower() == username.lower()

    def get_book_sections(self, user):
        return [
            ("Запланировано", user.profile.planned.all()),
            ("Читаю", user.profile.reading.all()),
            ("Брошено", user.profile.dropped.all()),
            ("Прочитано", user.profile.finished.all()),
        ]

    def get_context(self, user, u_form=None, p_form=None):
        return {
            "user": user,
            "u_form": u_form or UserUpdateForm(instance=user),
            "p_form": p_form or ProfileUpdateForm(instance=user.profile),
            "book_sections": self.get_book_sections(user),
            "orders": user.orders.all(),
        }

    def get(self, request, username, *args, **kwargs):
        user = get_object_or_404(User, username__iexact=username)
        context = self.get_context(user)
        return render(request, "users/profile.html", context)

    def post(self, request, username, *args, **kwargs):
        user = get_object_or_404(User, username__iexact=username)
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Ваша летопись обновлена с великим успехом.")
            return redirect("profile", username=user.username)

        context = self.get_context(user, u_form, p_form)
        return render(request, "users/profile.html", context)


class AddBookToListView(LoginRequiredMixin, View):
    def post(self, request, username, *args, **kwargs):
        if request.user.username.lower() != username.lower():
            return HttpResponseForbidden("Нельзя изменять чужой список.")

        profile = request.user.profile
        book_id = request.POST.get("book_id")
        list_name = request.POST.get("list_name")

        if list_name not in LIST_NAMES:
            return JsonResponse({"error": "Некорректный список."}, status=400)
        if not book_id:
            return JsonResponse({"error": "book_id не передан."}, status=400)

        book = get_object_or_404(Book, id=book_id)

        for name in LIST_NAMES:
            getattr(profile, name).remove(book)

        getattr(profile, list_name).add(book)

        messages.success(
            request, f'Книга "{book.title}" добавлена в список "{list_name}".'
        )
        return redirect("profile", username=username)


class RemoveBookFromListView(LoginRequiredMixin, View):
    def post(self, request, username, *args, **kwargs):
        if request.user.username.lower() != username.lower():
            return HttpResponseForbidden("Нельзя изменять чужой список.")

        profile = request.user.profile
        book_id = request.POST.get("book_id")

        if not book_id:
            return JsonResponse({"error": "book_id не передан."}, status=400)

        book = get_object_or_404(Book, id=book_id)

        removed_from = []
        for name in LIST_NAMES:
            book_list = getattr(profile, name)
            if book in book_list.all():
                book_list.remove(book)
                removed_from.append(name)

        if removed_from:
            messages.success(
                request,
                f'Книга "{book.title}" удалена из списков: {", ".join(removed_from)}.',
            )
        else:
            messages.info(request, f'Книга "{book.title}" не была в списках.')

        return redirect("profile", username=username)
