from django import forms

class SearchForm(forms.Form):
    check_in = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    check_out = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    guests = forms.IntegerField(min_value=1, initial=1)

class ReservationForm(forms.Form):
    holder_name = forms.CharField(max_length=120)
    holder_email = forms.EmailField()

class CheckoutForm(forms.Form):
    check_in = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    check_out = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    guests = forms.IntegerField(min_value=1, initial=1)
    holder_name = forms.CharField(label="Nombre completo", max_length=120)
    holder_email = forms.EmailField(label="Email")
    nationality = forms.CharField(label="Nacionalidad (opcional)", max_length=60, required=False)
