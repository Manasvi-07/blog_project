from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["first_name","email"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered")
        return email

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("password2"):
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.first_name = self.cleaned_data["first_name"]
        if commit:
            user.save()
        return user


class EmailLoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)
            if self.user is None:
                raise forms.ValidationError("Invalid email or password")
            if not self.user.is_active:
                raise forms.ValidationError("This account is inactive")
        return cleaned_data

    def get_user(self):
        return self.user
