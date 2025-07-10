from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import QuerySet
from django.utils.http import url_has_allowed_host_and_scheme
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView

from my_polls.users.models import User


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["first_name", "last_name"]
    success_message = _("Information successfully updated")

    def get_success_url(self) -> str:
        return self.request.META.get("HTTP_REFERER") or "/"

    def get_object(self, queryset: QuerySet | None=None) -> User:
        assert self.request.user.is_authenticated
        return self.request.user


user_update_view = UserUpdateView.as_view()

