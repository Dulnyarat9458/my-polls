
from django.urls import path

from my_polls.polls import views

app_name = "polls"

urlpatterns = [
    path("", view=views.PollsView.as_view(), name="index"),
    path("add/", view=views.AddPollView.as_view(), name="add"),
    path("<int:pk>/", view=views.PollDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", view=views.EditPollView.as_view(), name="edit"),
    path("<int:pk>/delete/", view=views.DeletePollView.as_view(), name="delete"),
]
