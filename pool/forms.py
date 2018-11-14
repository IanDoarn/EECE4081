from django import forms


class BetForm(forms.Form):
    amount = forms.CharField(max_length=30)

    def clean(self):
        cleaned_data = super(BetForm, self).clean()
        amount = cleaned_data.get('amount')
