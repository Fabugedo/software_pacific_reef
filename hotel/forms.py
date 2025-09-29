from django import forms

class SearchForm(forms.Form):
    check_in = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    check_out = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    guests = forms.IntegerField(min_value=1, initial=1)

class ReservationForm(forms.Form):
    holder_name = forms.CharField(max_length=120)
    holder_email = forms.EmailField()
