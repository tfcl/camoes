
from .models import Book,Author,Publisher
from django import forms



class BookCreateForm(forms.ModelForm):
    class Meta:
        fields = ('title','year','classification','isbn','publisher','authors',)
        model = Book

class AuthorCreateForm(forms.ModelForm):
    class Meta:
        fields = ('name','deathYear','birthYear',)
        model = Author

class PublisherCreateForm(forms.ModelForm):
    class Meta:
        fields = ('name','adress',)
        model = Publisher