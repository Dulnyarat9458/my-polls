from django import forms

from my_polls.polls.models import Poll


class PollModelForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['question']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_question(self):
        question = self.cleaned_data.get('question')
        if not question:
            raise forms.ValidationError("This field is required.")
        return question
