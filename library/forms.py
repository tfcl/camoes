
from .models import Requisition,Book,Author,Publisher
from django import forms


class RequisitionCreateForm(forms.ModelForm):
    class Meta:
        fields = ('book','user',)
        model = Requisition

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