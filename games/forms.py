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

    def clean_title(self):
        title = self.cleaned_data["title"].strip()

        if not title:
            raise forms.ValidationError(
                "Game title cannot be empty."
            )

        return title


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

    def clean_rating(self):
        rating = self.cleaned_data.get("rating")

        if rating is not None and not 0 <= rating <= 10:
            raise forms.ValidationError(
                "Rating must be between 0 and 10."
            )

        return rating

    def clean_completion(self):
        completion = self.cleaned_data.get("completion")

        if completion is None:
            return 0

        if not 0 <= completion <= 100:
            raise forms.ValidationError(
                "Completion must be between 0 and 100."
            )

        return completion