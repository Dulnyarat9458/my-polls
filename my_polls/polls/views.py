import json

from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count

from my_polls.polls.models import Poll, Choice
from my_polls.polls.forms import PollModelForm
from my_polls.polls.formsets import ChoiceInlineFormSet


class PollsView(LoginRequiredMixin, ListView):
    template_name = "pages/polls/poll_index.html"
    context_object_name = "polls"

    def get_queryset(self):
        return Poll.objects.filter(user=self.request.user)


class PollDetailView(LoginRequiredMixin, DetailView):
    template_name = "pages/polls/poll_detail.html"
    context_object_name = "poll"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        choices = self.object.choice_set.annotate(vote_count=Count('vote'))

        context["choice_labels"] = json.dumps([choice.choice_text for choice in choices], ensure_ascii=False)
        context["choice_counts"] = json.dumps([choice.vote_count for choice in choices])
            
        return context

    def get_queryset(self):
        return Poll.objects.filter(user=self.request.user).prefetch_related('choice_set')


class AddPollView(LoginRequiredMixin, CreateView):
    template_name = "pages/polls/poll_add.html"
    form_class = PollModelForm
    success_url = reverse_lazy("polls:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ChoiceInlineFormSet(self.request.POST)
        else:
            context['formset'] = ChoiceInlineFormSet()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)



class EditPollView(LoginRequiredMixin, UpdateView):
    template_name = "pages/polls/poll_edit.html"
    context_object_name = "poll"
    form_class = PollModelForm
    success_url = reverse_lazy("polls:index")

    def get_queryset(self):
        return Poll.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ChoiceInlineFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = ChoiceInlineFormSet(instance=self.object)
        
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            submitted_ids = set()
            for subform in formset.forms:
                if subform.cleaned_data.get("DELETE"):
                    continue
                instance = subform.cleaned_data.get("id")
                if instance:
                    submitted_ids.add(instance.pk)
            Choice.objects.filter(poll=self.object).exclude(pk__in=submitted_ids).delete()
            formset.save()
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)


class DeletePollView(LoginRequiredMixin, DeleteView):
    template_name = "pages/polls/poll_delete.html"
    context_object_name = "poll"
    model = Poll
    success_url = reverse_lazy("polls:index")

    def get_queryset(self):
        return Poll.objects.filter(user=self.request.user)
