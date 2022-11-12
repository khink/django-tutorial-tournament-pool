from django.test import TestCase

from tournaments.models import Team, Tournament
from .models import Prediction


class PredictionModelTests(TestCase):
    def test_string_representation(self):
        """
        The string representation should include name, tournament and winning team.
        """
        tournament = Tournament(name="Soccer Worlds 2022")
        team = Team(name="Netherlands", tournament=tournament)
        prediction = Prediction(name="Joe", tournament=tournament, winning_team=team)
        self.assertIn("Joe", str(prediction))
        self.assertIn("Netherlands", str(prediction))
        self.assertIn("Soccer Worlds 2022", str(prediction))
