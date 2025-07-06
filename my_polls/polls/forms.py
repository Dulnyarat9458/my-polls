from django import forms

from my_polls.polls.models import Poll, Choice


class PollModelForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['question']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ChoiceModelForm(forms.ModelForm):
    
    choice_text = forms.CharField(
        required=True,
        max_length=255,
    )
    class Meta:
        model = Choice
        fields = ['choice_text']
        widgets = {
            'choice_text': forms.TextInput(attrs={'class': 'form-control'}),
        }
