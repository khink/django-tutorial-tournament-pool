from django.test import TestCase

from .models import Team, Tournament


class TournamentModelTests(TestCase):
    def test_string_representation(self):
        """
        The string representation should include name.
        """
        tournament = Tournament(name="Soccer Worlds 2022")
        self.assertIn("Soccer Worlds 2022", str(tournament))


class TeamModelTests(TestCase):
    def test_string_representation(self):
        """
        The string representation should include name.
        """
        team = Team(name="Netherlands")
        self.assertIn("Netherlands", str(team))
