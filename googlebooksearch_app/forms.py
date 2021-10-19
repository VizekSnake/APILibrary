from django import forms
from googlebooksearch_app.models import Book


class BooksSearchForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn']


class NumberInput(forms.NumberInput):
    input_type = 'number'


class BookAddForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

    widgets = {
        'publication_date': NumberInput(attrs={'min': 1, 'max': '4', 'type': 'number'}),
    }


class SearchBookForm(forms.Form):
    q = forms.CharField(label_suffix='Book info to find in Google library')


class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

    widgets = {
        'publication_date': NumberInput(attrs={'min': 1, 'max': '4', 'type': 'number'}),
    }
