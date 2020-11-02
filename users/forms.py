from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile 
from django.core.validators import ValidationError
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileCreateForm(forms.ModelForm):
    class Meta:
        fields = ('number','telephone','adress', )
        model = Profile