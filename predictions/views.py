from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from tournaments.models import Team, Tournament

from .models import Prediction


def create(request):
    try:
        tournament = Tournament.objects.last()
    except Tournament.DoesNotExist:
        raise Http404("No tournament exists. Create one in the admin.")

    try:
        selected_team = tournament.team_set.get(pk=request.POST["team"])
    except (KeyError, Team.DoesNotExist):
        # Redisplay the form.
        teams = tournament.team_set.all()
        return render(
            request,
            "predictions/prediction_form.html",
            {
                "tournament_name": tournament.name,
                "team_list": teams,
                "error_message": "You didn't pick a team yet.",
            },
        )
    else:
        prediction = Prediction(tournament=tournament, winning_team=selected_team)
        prediction.save()

        # We're just going to redirect to the tournaments list for now.
        return HttpResponseRedirect(reverse("tournaments:index"))
