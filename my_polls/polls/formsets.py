from django.forms import inlineformset_factory, BaseInlineFormSet

from my_polls.polls.models import Poll, Choice
from my_polls.polls.forms import ChoiceModelForm


class RequiredInlineFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False
            
            
ChoiceInlineFormSet = inlineformset_factory(
    Poll, Choice,
    form=ChoiceModelForm,
    formset=RequiredInlineFormSet, 
    extra=0,
    can_delete=True,
    min_num=1,
    validate_min=True
)