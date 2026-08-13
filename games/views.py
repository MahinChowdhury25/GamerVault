from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import GameEntryForm, GameForm
from .models import Genre, Platform


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


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def dashboard_view(request):
    game_entries = request.user.game_entries.all()

    total_games = game_entries.count()

    playing_count = game_entries.filter(
        status="playing"
    ).count()

    completed_count = game_entries.filter(
        status="completed"
    ).count()

    wishlist_count = game_entries.filter(
        status="wishlist"
    ).count()

    dropped_count = game_entries.filter(
        status="dropped"
    ).count()

    recent_games = game_entries.select_related(
        "game",
        "game__genre",
        "game__platform",
    )[:5]

    context = {
        "total_games": total_games,
        "playing_count": playing_count,
        "completed_count": completed_count,
        "wishlist_count": wishlist_count,
        "dropped_count": dropped_count,
        "recent_games": recent_games,
    }

    return render(
        request,
        "games/dashboard.html",
        context,
    )


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
        .select_related(
            "game",
            "game__genre",
            "game__platform",
        )
        .all()
    )

    search_query = request.GET.get("search", "").strip()
    status_filter = request.GET.get("status", "").strip()
    genre_filter = request.GET.get("genre", "").strip()
    platform_filter = request.GET.get("platform", "").strip()

    if search_query:
        game_entries = game_entries.filter(
            game__title__icontains=search_query
        )

    if status_filter:
        game_entries = game_entries.filter(
            status=status_filter
        )

    if genre_filter:
        game_entries = game_entries.filter(
            game__genre_id=genre_filter
        )

    if platform_filter:
        game_entries = game_entries.filter(
            game__platform_id=platform_filter
        )

    context = {
        "game_entries": game_entries,
        "search_query": search_query,
        "status_filter": status_filter,
        "genre_filter": genre_filter,
        "platform_filter": platform_filter,
        "genres": Genre.objects.all(),
        "platforms": Platform.objects.all(),
    }

    return render(
        request,
        "games/library.html",
        context,
    )


@login_required
def edit_game_view(request, entry_id):
    game_entry = request.user.game_entries.select_related(
        "game"
    ).filter(id=entry_id).first()

    if game_entry is None:
        messages.error(request, "Game not found.")
        return redirect("library")

    if request.method == "POST":
        game_form = GameForm(
            request.POST,
            request.FILES,
            instance=game_entry.game,
        )

        entry_form = GameEntryForm(
            request.POST,
            instance=game_entry,
        )

        if game_form.is_valid() and entry_form.is_valid():
            game_form.save()
            entry_form.save()

            messages.success(
                request,
                f"{game_entry.game.title} was updated successfully!"
            )

            return redirect("library")

    else:
        game_form = GameForm(instance=game_entry.game)
        entry_form = GameEntryForm(instance=game_entry)

    context = {
        "game_form": game_form,
        "entry_form": entry_form,
        "game_entry": game_entry,
    }

    return render(request, "games/edit_game.html", context)


@login_required
def delete_game_view(request, entry_id):
    game_entry = request.user.game_entries.select_related(
        "game"
    ).filter(id=entry_id).first()

    if game_entry is None:
        messages.error(request, "Game not found.")
        return redirect("library")

    if request.method == "POST":
        game_title = game_entry.game.title

        game_entry.delete()

        messages.success(
            request,
            f"{game_title} was removed from your library."
        )

        return redirect("library")

    return render(
        request,
        "games/delete_game.html",
        {"game_entry": game_entry},
    )