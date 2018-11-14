from django import forms


class BetForm(forms.Form):
    amount = forms.CharField(max_length=30)
    favorite = forms.BooleanField()
    underdog = forms.BooleanField()
    high_risk = forms.BooleanField()

    def clean(self):
        cleaned_data = super(BetForm, self).clean()
        amount = cleaned_data.get('amount')
        favorite = cleaned_data.get('favorite')
        underdog = cleaned_data.get('underdog')
        high_risk = cleaned_data.get('high_risk')

