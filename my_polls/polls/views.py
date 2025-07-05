from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from my_polls.polls.models import Poll
from my_polls.polls.forms import PollModelForm


class PollsView(ListView):
    template_name = "pages/polls/poll_index.html"
    context_object_name = "polls"

    def get_queryset(self):
        return Poll.objects.filter(user=self.request.user)


class PollDetailView(DetailView):
    template_name = "pages/polls/poll_detail.html"
    context_object_name = "poll"
    model = Poll


class AddPollView(CreateView):
    template_name = "pages/polls/poll_add.html"
    form_class = PollModelForm
    success_url = reverse_lazy("polls:index")
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form) 


class EditPollView(UpdateView):
    template_name = "pages/polls/poll_edit.html"
    context_object_name = "poll"
    model = Poll
    form_class = PollModelForm
    success_url = reverse_lazy("polls:index")

    def form_valid(self, form):
        form.save(user=self.request.user)
        return super().form_valid(form)
    

class DeletePollView(DeleteView):
    template_name = "pages/polls/poll_delete.html"
    context_object_name = "poll"
    model = Poll
    success_url = reverse_lazy("polls:index")

    def form_valid(self, form):
        print("Deleting poll:", self.object)
        return super().form_valid(form)
