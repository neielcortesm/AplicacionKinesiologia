from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(forms.Form):
    email = forms.EmailField(label="Correo")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=False, label="Nombres")
    last_name = forms.CharField(required=False, label="Apellidos")
    email = forms.EmailField(label="Correo electrónico")

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data["email"].lower().strip()
        user.email = email
        user.username = email  # importante
        if commit:
            user.save()
        return user
