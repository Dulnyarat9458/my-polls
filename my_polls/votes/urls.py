
from django.urls import path

from my_polls.votes import views

app_name = "votes"

urlpatterns = [
    path("<int:pk>/", view=views.VoteView.as_view(), name="vote"),
]
