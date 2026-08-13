from django import forms

from .models import Game, GameEntry


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = [
            "title",
            "genre",
            "platform",
            "cover_image",
            "description",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Enter game title",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Enter a short description...",
                    "rows": 5,
                }
            ),
        }


class GameEntryForm(forms.ModelForm):
    class Meta:
        model = GameEntry
        fields = [
            "status",
            "rating",
            "completion",
            "review",
        ]

        widgets = {
            "rating": forms.NumberInput(
                attrs={
                    "min": 0,
                    "max": 10,
                    "placeholder": "0 - 10",
                }
            ),
            "completion": forms.NumberInput(
                attrs={
                    "min": 0,
                    "max": 100,
                    "placeholder": "0 - 100%",
                }
            ),
            "review": forms.Textarea(
                attrs={
                    "placeholder": "Write your thoughts about the game...",
                    "rows": 5,
                }
            ),
        }