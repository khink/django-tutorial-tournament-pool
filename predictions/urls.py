from django.urls import path

from . import views

app_name = "predictions"
urlpatterns = [
    path("", views.PredictionListView.as_view(), name="list"),
    path("vote/", views.create, name="vote"),
]
