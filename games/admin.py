from django.contrib import admin
from .models import Genre, Platform, Game, GameEntry


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("title", "genre", "platform")
    search_fields = ("title",)
    list_filter = ("genre", "platform")


@admin.register(GameEntry)
class GameEntryAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "game",
        "status",
        "rating",
        "completion",
        "date_added",
    )
    list_filter = ("status",)
    search_fields = ("user__username", "game__title")