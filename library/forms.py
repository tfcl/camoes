
from .models import Book,Author,Publisher,Category
from django import forms



class BookCreateForm(forms.ModelForm):
    class Meta:
        fields = ('title','year','classification','isbn','publisher','authors','category',)
        model = Book
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['category'].queryset=Category.objects.filter(depth=0)

class AuthorCreateForm(forms.ModelForm):
    class Meta:
        fields = ('name','deathYear','birthYear',)
        model = Author

class PublisherCreateForm(forms.ModelForm):
    class Meta:
        fields = ('name','adress',)
        model = Publisher