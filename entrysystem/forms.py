from .models import NewUser
from django.contrib.auth.forms import UserCreationForm
from django import forms
from random import randint


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    usertype = forms.ChoiceField(choices=NewUser.user_type)

    class Meta:
        model = NewUser
        fields = ['username', 'email', 'usertype', 'password1', 'password2']


def generate_visit_code():
    code = ""
    for i in range(6):
        code += str(randint(0, 9))
    return code
