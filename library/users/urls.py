from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.views import (AddBookToListView, ProfileView,
                         RedirectToOwnProfileView, RegisterView,
                         RemoveBookFromListView)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path(
        "logout/", LogoutView.as_view(template_name="users/logout.html"), name="logout"
    ),
    path(
        "profile/<str:username>/add-book/", AddBookToListView.as_view(), name="add-book"
    ),
    path(
        "profile/<str:username>/remove-book/",
        RemoveBookFromListView.as_view(),
        name="remove-book",
    ),
    path("profile/<str:username>", ProfileView.as_view(), name="profile"),
    path("profile/", RedirectToOwnProfileView.as_view(), name="profile"),
]
