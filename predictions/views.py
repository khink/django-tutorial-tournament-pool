from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from tournaments.models import Team, Tournament

from .models import Prediction


def create(request):
    # This is very arbitrary, but we're ONLY interested in the last tournament.
    tournament = Tournament.objects.last()

    if not tournament:
        raise Http404("No tournament exists. Create one in the admin.")

    try:
        selected_team = tournament.team_set.get(pk=request.POST["team"])
        name = request.POST["name"]
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
        prediction = Prediction(
            tournament=tournament, winning_team=selected_team, name=name
        )
        prediction.save()

        return HttpResponseRedirect(reverse("predictions:list"))


class PredictionListView(generic.ListView):
    template_name = "predictions/prediction_list.html"
    context_object_name = "prediction_list"

    def get_queryset(self):
        tournament = Tournament.objects.last()
        if not tournament:
            raise Http404()

        return tournament.prediction_set.all()
