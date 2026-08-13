from django.contrib.auth.models import User
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Platform(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Game(models.Model):
    title = models.CharField(max_length=200)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="games",
    )
    platform = models.ForeignKey(
        Platform,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="games",
    )
    cover_image = models.ImageField(
        upload_to="game_covers/",
        blank=True,
        null=True,
    )
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class GameEntry(models.Model):

    STATUS_CHOICES = [
        ("wishlist", "Wishlist"),
        ("playing", "Playing"),
        ("completed", "Completed"),
        ("dropped", "Dropped"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="game_entries",
    )

    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name="entries",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="wishlist",
    )

    rating = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    completion = models.PositiveIntegerField(
        default=0,
    )

    review = models.TextField(blank=True)

    date_added = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_added"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "game"],
                name="unique_user_game",
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.game.title}"