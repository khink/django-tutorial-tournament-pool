from django.db import models

from tournaments.models import Team, Tournament


class Prediction(models.Model):
    name = models.CharField(max_length=200)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    winning_team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} predicts {self.winning_team} will win {self.tournament}"
