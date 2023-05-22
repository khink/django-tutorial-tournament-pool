from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django_webtest import WebTest

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


class PredictionWebTests(WebTest):
    def test_cast_prediction(self):
        """
        We should be able to cast a prediction.
        """
        tournament = Tournament.objects.create(name="Soccer Worlds 2022")
        team = Team.objects.create(name="Netherlands", tournament=tournament)
        response = self.app.get(reverse("predictions:vote"))
        assert response.status_code == 200
        assert f"Who will win {tournament}?" in response

        # Play around with Webtest's form API
        form = response.form
        field = form["team"]
        assert field.options == [(str(team.pk), False, None)]
        assert field.value == None

        # Select a team and submit
        form["team"] = team.pk
        form["name"] = "John Doe"
        post_submit_page = form.submit().follow()
        assert post_submit_page.request.path == reverse(
            "predictions:list"
        ), "We should be redirected to the predictions list"
        assert Prediction.objects.count() == 1, "A Prediction should have been created"
        prediction = Prediction.objects.get()
        assert prediction.winning_team == team
        assert prediction.name == "John Doe"


class AdminWebTests(WebTest):
    def test_create_prediction(self):
        admin_user = User.objects.create_superuser(
            "admin", "admin@example.com", "secret"
        )
        tournament = Tournament.objects.create(name="Soccer Worlds 2022")
        team = Team.objects.create(name="Netherlands", tournament=tournament)
        self.assertEqual(Prediction.objects.exists(), False)

        changelist_url = reverse("admin:predictions_prediction_changelist")
        predictions_changelist_page = self.app.get(changelist_url, user="admin")
        add_prediction_page = predictions_changelist_page.click("Add prediction")

        assert tournament.name in add_prediction_page
        assert team.name in add_prediction_page
        form = add_prediction_page.forms["prediction_form"]
        form["name"] = "My prediction"
        form["tournament"] = tournament.pk
        form["winning_team"] = team.pk
        result_page = form.submit().follow()
        assert result_page.request.path == changelist_url

        assert Prediction.objects.count() == 1
        prediction = Prediction.objects.get()
        assert prediction.name == "My prediction"


def test_create_prediction_pytest(django_app, admin_user):
    tournament = Tournament.objects.create(name="Soccer Worlds 2022")
    team = Team.objects.create(name="Netherlands", tournament=tournament)
    assert Prediction.objects.exists() is False

    changelist_url = reverse("admin:predictions_prediction_changelist")
    predictions_changelist_page = django_app.get(changelist_url, user=admin_user)
    add_prediction_page = predictions_changelist_page.click("Add prediction")

    assert tournament.name in add_prediction_page
    assert team.name in add_prediction_page
    form = add_prediction_page.forms["prediction_form"]
    form["name"] = "My prediction"
    form["tournament"] = tournament.pk
    form["winning_team"] = team.pk
    result_page = form.submit().follow()
    assert result_page.request.path == changelist_url

    assert Prediction.objects.count() == 1
    prediction = Prediction.objects.get()
    assert prediction.name == "My prediction"
