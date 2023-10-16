from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User
from django import forms


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']
    pass


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'description', 'train', 'score']
        exclude = []
        widgets = {
            'score' : forms.TextInput(attrs = {'placeholder': '88 очков'}),
        }
        


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']
        widgets = {
            'avatar': forms.TextInput(attrs={'placeholder': 'аватар', "title": "аватар"}),
            'name': forms.TextInput(attrs={'placeholder': 'имя', "title": "имя"}),
            'username': forms.TextInput(attrs={'placeholder': 'логин', "title": "логин"}),
            'bio': forms.TextInput(attrs={'placeholder': 'био', "title": "био"}),
        }
