from django.http import HttpResponse
from django.template import loader

from .models import Tournament


def index(request):
    tournaments = Tournament.objects.all()
    template = loader.get_template("tournaments/index.html")
    context = {
        "tournament_list": tournaments,
    }
    return HttpResponse(template.render(context, request))


def detail(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    teams = tournament.team_set.all()
    template = loader.get_template("tournaments/detail.html")
    context = {
        "tournament_name": tournament.name,
        "team_list": teams,
    }
    return HttpResponse(template.render(context, request))
