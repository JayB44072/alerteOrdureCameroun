from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class InscriptionForm(UserCreationForm):
    email = forms.EmailField(required=True)
    ville = forms.CharField(max_length=100, required=True)
    quartier = forms.CharField(max_length=100, required=True)
    role = forms.ChoiceField(
        choices=(
            ('citoyen', 'Citoyen'),
            ('agent', 'Agent HYSACAM'),
        ),
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'ville', 'quartier', 'role', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class ConnexionForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})