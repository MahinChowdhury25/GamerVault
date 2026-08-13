from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import GameEntryForm, GameForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        password_confirm = request.POST.get("password_confirm", "")

        if not username or not email or not password:
            messages.error(request, "Please fill in all fields.")
            return render(request, "games/register.html")

        if password != password_confirm:
            messages.error(request, "Passwords do not match.")
            return render(request, "games/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "That username is already taken.")
            return render(request, "games/register.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "That email is already registered.")
            return render(request, "games/register.html")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        login(request, user)
        return redirect("dashboard")

    return render(request, "games/register.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        messages.error(request, "Invalid username or password.")

    return render(request, "games/login.html")


@login_required
def dashboard_view(request):
    return render(request, "games/dashboard.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def add_game_view(request):
    if request.method == "POST":
        game_form = GameForm(request.POST, request.FILES)
        entry_form = GameEntryForm(request.POST)

        if game_form.is_valid() and entry_form.is_valid():
            game = game_form.save()

            game_entry = entry_form.save(commit=False)
            game_entry.user = request.user
            game_entry.game = game
            game_entry.save()

            messages.success(
                request,
                f"{game.title} was added to your library!"
            )

            return redirect("library")

    else:
        game_form = GameForm()
        entry_form = GameEntryForm()

    context = {
        "game_form": game_form,
        "entry_form": entry_form,
    }

    return render(request, "games/add_game.html", context)


@login_required
def library_view(request):
    game_entries = (
        request.user.game_entries
        .select_related("game", "game__genre", "game__platform")
        .all()
    )

    return render(
        request,
        "games/library.html",
        {"game_entries": game_entries},
    )