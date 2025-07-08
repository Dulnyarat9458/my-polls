from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseRedirect
from django.contrib import messages

from my_polls.polls.models import Poll
from my_polls.votes.forms import VoteForm
from my_polls.votes.models import Vote


class VoteView(SingleObjectMixin, FormView):
    template_name = 'pages/votes/vote_form.html'
    form_class = VoteForm
    model = Poll
    success_url = reverse_lazy("votes:vote")
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def get_initial(self):
        initial = super().get_initial()
        poll = self.get_object()
        user = self.request.user
        try:
            vote = Vote.objects.get(choice__poll=poll, user=user)
            initial['choice'] = vote.choice
        except Vote.DoesNotExist:
            pass
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['poll'] = self.get_object()
        return kwargs

    def get_success_url(self):
        messages.success(self.request, "Voting successful!")
        return reverse_lazy("votes:vote", kwargs={"pk": self.object.pk})
    
    def form_valid(self, form):
        poll = self.get_object()
        if poll.is_closed:
            messages.error(self.request, "This poll is closed. Voting is disabled.")
            return HttpResponseRedirect(reverse_lazy("votes:vote", kwargs={"pk": self.object.pk}))
        
        user = self.request.user
        vote, created = Vote.objects.update_or_create(
            user=user,
            choice__poll=poll,
            defaults={'choice': form.cleaned_data['choice']}
        )
        return super().form_valid(form)
