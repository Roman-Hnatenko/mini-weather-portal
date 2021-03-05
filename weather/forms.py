from django import forms


class CityForm(forms.Form):
    city = forms.CharField(label='City', max_length=25)

    def clean(self):
        cleaned_data = super().clean()
        if not str(self.data.get('city')).isalpha():
            raise forms.ValidationError('')
        return cleaned_data
