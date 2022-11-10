from django.shortcuts import get_object_or_404, render

from .models import Tournament


def index(request):
    tournaments = Tournament.objects.all()
    context = {
        "tournament_list": tournaments,
    }
    return render(request, "tournaments/index.html", context)


def detail(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    teams = tournament.team_set.all()
    context = {
        "tournament_name": tournament.name,
        "team_list": teams,
    }
    return render(request, "tournaments/detail.html", context)
