from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile 
from django.core.validators import ValidationError
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField(label='Numero de Aluno')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirme a Password', widget=forms.PasswordInput)
    

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None
            
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("O Email já existe")
        return email
    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2']
        help_texts = {
            'password1': None,
            'password2': None,
        }

class ProfileCreateForm(forms.ModelForm):
    class Meta:
        
        model = Profile
        fields=['address','name','contact' ]