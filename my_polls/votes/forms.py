from django import forms

from my_polls.votes.models import Vote
from my_polls.polls.models import Poll


class VoteForm(forms.ModelForm):

    
    class Meta:
        model = Vote
        fields = ['choice']
        widgets = {
            'choice': forms.RadioSelect(),
        }
        
    def __init__(self, *args, **kwargs):
        poll = kwargs.pop('poll', None)
        super().__init__(*args, **kwargs)
        if poll:
            self.fields['choice'].choices = [(choice.id, choice.choice_text) for choice in poll.choice_set.all()]