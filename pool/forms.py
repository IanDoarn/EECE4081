from django import forms


class BetForm(forms.Form):
    favorite = forms.BooleanField()
    underdog = forms.BooleanField()
    high_risk = forms.BooleanField(required=False)

    def clean(self):
        cleaned_data = super(BetForm, self).clean()
        favorite = cleaned_data.get('favorite')
        underdog = cleaned_data.get('underdog')
        high_risk = cleaned_data.get('high_risk')

