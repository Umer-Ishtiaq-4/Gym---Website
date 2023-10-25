from django import forms
from django.contrib.auth.forms import UserCreationForm
from userprofile.models import User  # Import your custom User model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')  # Include the fields you want in the form
