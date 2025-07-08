import json
import csv
from datetime import datetime

from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.utils.text import slugify
from django.contrib import messages

from my_polls.polls.models import Poll, Choice
from my_polls.polls.forms import PollModelForm
from my_polls.polls.formsets import ChoiceInlineFormSet


class PollsView(LoginRequiredMixin, ListView):
    template_name = "pages/polls/poll_index.html"
    context_object_name = "polls"
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        querydict = self.request.GET.copy()
        querydict.pop('page', None)
        preserved_query = querydict.urlencode()
        context['preserved_query'] = preserved_query
        return context

    def get_queryset(self):
        search = self.request.GET.get('search')
        order = self.request.GET.get('order')
        polls = Poll.objects.filter(user=self.request.user)
        if search:
            polls = polls.filter(question__icontains=search)
        if order == 'updated':
            polls = polls.order_by('-updated_at')
        elif order == 'updated_asc':
            polls = polls.order_by('updated_at')
        elif order == 'question':
            polls = polls.order_by('question')
        else:
            polls = polls.order_by('-updated_at')
        return polls


class PollDetailView(LoginRequiredMixin, DetailView):
    template_name = "pages/polls/poll_detail.html"
    context_object_name = "poll"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        choices = self.object.choice_set.annotate(vote_count=Count('vote'))
        context["choice_labels"] = json.dumps(
            [choice.choice_text for choice in choices], 
            ensure_ascii=False
        )
        context["choice_counts"] = json.dumps(
            [choice.vote_count for choice in choices]
        )
        
        vote = self.request.build_absolute_uri(
            reverse("votes:vote", kwargs={"pk": self.object.pk})
        )
        context["vote_url"] = vote
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
            messages.success(self.request, "Poll successfully added!")
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)


class EditPollView(LoginRequiredMixin, UpdateView):
    template_name = "pages/polls/poll_edit.html"
    context_object_name = "poll"
    form_class = PollModelForm
    
    def get_success_url(self):
        messages.success(self.request, "Poll successfully updated!")
        return reverse_lazy("polls:detail", kwargs={"pk": self.object.pk})

    def get_queryset(self):
        return Poll.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ChoiceInlineFormSet(
                self.request.POST, 
                instance=self.object
            )
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
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)


class DeletePollView(LoginRequiredMixin, DeleteView):
    template_name = "pages/polls/poll_delete.html"
    context_object_name = "poll"
    model = Poll
    success_url = reverse_lazy("polls:index")

    def get_success_url(self):
        messages.success(self.request, "Poll successfully deleted!")
        return self.success_url

    def get_queryset(self):
        return Poll.objects.filter(user=self.request.user)


class PollVotesDownloadView(LoginRequiredMixin, DetailView):
    model = Poll

    def get_queryset(self):
        return Poll.objects.filter(user=self.request.user)

    def render_to_response(self, context, **response_kwargs):
        poll = self.get_object()        
        choices = poll.choice_set.annotate(vote_count=Count('vote'))\
            .order_by('-vote_count', 'choice_text')
        response = HttpResponse(content_type='text/csv')
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        safe_question = slugify(poll.question)
        filename = f'poll-{poll.id}-votes-{now}.csv'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        writer = csv.writer(response)
        writer.writerow(['Choice', 'Vote Count'])
        for choice in choices:
            writer.writerow([choice.choice_text, choice.vote_count])
        return response
