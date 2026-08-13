from django.urls import path

from .views import (
    add_game_view,
    dashboard_view,
    library_view,
    login_view,
    logout_view,
    register_view,
)

urlpatterns = [
    path("", dashboard_view, name="dashboard"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    path("library/", library_view, name="library"),
    path("library/add/", add_game_view, name="add_game"),
]