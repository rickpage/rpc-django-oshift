from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(
        label="First Name",
        widget=forms.TextInput,
    )
    last_name = forms.CharField(
        label="Last Name",
        widget=forms.TextInput,
    )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        # Making email not required
        self.fields['email'].required = False
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False

    class Meta:
        model = User
        fields = ("username", "email", "first_name","last_name","password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
        return user
