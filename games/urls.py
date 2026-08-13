from django.urls import path

from .views import (
    add_game_view,
    dashboard_view,
    delete_game_view,
    edit_game_view,
    game_detail_view,
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

    path(
        "library/<int:entry_id>/",
        game_detail_view,
        name="game_detail",
    ),

    path(
        "library/<int:entry_id>/edit/",
        edit_game_view,
        name="edit_game",
    ),

    path(
        "library/<int:entry_id>/delete/",
        delete_game_view,
        name="delete_game",
    ),
]