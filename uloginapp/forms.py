from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class UserRegisterForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput(), required=True)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторить пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['username'].widget.attrs['class'] = 'input'
        self.fields['username'].label = 'Никнейм'
        self.fields['email'].widget.attrs['class'] = 'input'
        self.fields['password1'].widget.attrs['class'] = 'input'
        self.fields['password2'].widget.attrs['class'] = 'input'

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        email = cleaned_data.get("email")

        if password1 != password2:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        username = self.cleaned_data["username"]
        if self.cleaned_data["username"] == "":
            self.cleaned_data["username"] = str(uuid.uuid4())
        user.username = self.cleaned_data["username"]
        user.password = make_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user