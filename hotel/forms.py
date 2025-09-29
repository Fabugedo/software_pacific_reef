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

class PaymentForm(forms.Form):
    method = forms.ChoiceField(
        label="Método de pago",
        choices=[("card", "Tarjeta de crédito/débito"), ("transfer", "Transferencia")],
        widget=forms.RadioSelect,
    )
    card_number = forms.CharField(
        label="N° tarjeta (simulado)",
        max_length=19,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "4111 1111 1111 1111"}),
    )
    accept = forms.BooleanField(label="Acepto términos y condiciones")
