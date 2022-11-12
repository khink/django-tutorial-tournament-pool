from django.urls import path

from . import views

app_name = "tournaments"
urlpatterns = [
    path("", views.TournamentIndexView.as_view(), name="index"),
    path("<int:pk>/", views.TournamentDetailView.as_view(), name="detail"),
]
