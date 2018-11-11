from django import forms
from django.forms import widgets

from .models import User


class LoginForm(forms.Form):
    """The simple form for log in into website and get all main features
    """
    email = forms.EmailField()
    password = forms.CharField(min_length=6, widget=forms.PasswordInput,
                               required=True)


class UserSignupForm(forms.ModelForm):
    """The form for creating new users for sign up on template.
    Includes all the required fields, plus a repeated password
    and send email verification for account activation.
    """
    birthday = forms.DateField(label='Birthday', widget=widgets.DateInput)
    password1 = forms.CharField(label='Password', max_length=60,
                                widget=widgets.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', max_length=60,
                                widget=widgets.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'country', 'city')

    def clean_password2(self):
        # Confirm if given password matched.
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match')
        return password2
