from django import forms


class BetForm(forms.Form):
    favorite = forms.BooleanField(required=False)
    underdog = forms.BooleanField(required=False)
    high_risk = forms.BooleanField(required=False)

    def clean(self):
        cleaned_data = super(BetForm, self).clean()
        favorite = cleaned_data.get('favorite')
        underdog = cleaned_data.get('underdog')
        high_risk = cleaned_data.get('high_risk')


