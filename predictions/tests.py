from django.test import TestCase
from django.urls import reverse

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


class PredictionIndexViewTests(TestCase):
    def test_no_tournaments(self):
        """
        If there are no tournaments, we should get a 404 Not Found.
        """
        response = self.client.get(reverse("predictions:list"))
        self.assertEqual(response.status_code, 404)

    def test_tournament_with_predictions(self):
        """
        If there is a tournaments, we should show its predictions.
        """
        tournament = Tournament.objects.create(name="Soccer Worlds 2022")
        team = Team.objects.create(name="Netherlands", tournament=tournament)
        prediction = Prediction.objects.create(
            name="Joe", tournament=tournament, winning_team=team
        )
        response = self.client.get(reverse("predictions:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(prediction))
