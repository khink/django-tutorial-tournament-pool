from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Tournament


class TournamentIndexView(generic.ListView):
    template_name = "tournaments/index.html"
    context_object_name = "tournament_list"

    def get_queryset(self):
        return Tournament.objects.all()


class TournamentDetailView(generic.DetailView):
    model = Tournament
    template_name = "tournaments/detail.html"
