from django.http import Http404
from django.shortcuts import render

from tournaments.models import Tournament


def create(request):
    try:
        tournament = Tournament.objects.last()
    except Tournament.DoesNotExist:
        raise Http404("No tournament exists. Create one in the admin.")
    teams = tournament.team_set.all()
    context = {
        "tournament_name": tournament.name,
        "team_list": teams,
    }
    return render(request, "predictions/prediction_form.html", context)
