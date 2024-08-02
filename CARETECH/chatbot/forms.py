from django import forms


class SymptomInputForm(forms.Form):
    symptom = forms.CharField(label='How do you Feel today:')


class SelectionForm(forms.Form):
    selection = forms.ChoiceField(choices=[], label='Select the one you meant:')
    days = forms.IntegerField(required=False, label='For how many days?')

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', [])
        super(SelectionForm, self).__init__(*args, **kwargs)
        self.fields['selection'].choices = choices
        if not choices:
            self.fields.pop('selection')
        else:
            self.fields.pop('days')
