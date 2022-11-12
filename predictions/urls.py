from django.urls import path

from . import views

app_name = "predictions"
urlpatterns = [
    path("", views.prediction_list, name="list"),
    path("vote/", views.create, name="vote"),
]
