from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("location/<str:location>", views.location, name="location"),
    path("check_favorite/<str:location>", views.check_favorite, name="check_favorite"),
    path("favorites", views.favorites, name="favorites"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]