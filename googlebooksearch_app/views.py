from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from googlebooksearch_app.models import Book
from googlebooksearch_app.forms import BooksSearchForm, BookAddForm, SearchBookForm
from django.contrib import messages
from datetime import datetime
from django.core.paginator import Paginator
import requests
import json
from googlebooksearch_app.serializers import BookSerializer
from rest_framework import generics
import environ

env = environ.Env()
env.read_env()
# Create your views here.
from googlebooksearch_app.services import get_books_data


class HomeView(View):
    def get(self, request):
        """  List of all books added to service"""
        books = Book.objects.all()
        book_searchform = BooksSearchForm(request.POST)
        return render(request, 'home.html', context={'books': books, 'book_searchform': book_searchform})

    def post(self, request):
        """  Filtering all books added to service by author, title or pub_date"""
        book_searchform = BooksSearchForm(request.POST)
        pub_date_from = request.POST.get('datepicker1')
        pub_date_to = request.POST.get('datepicker2')
        if book_searchform.is_valid():
            booktitle = book_searchform.cleaned_data.get('title')
            bookauthor = book_searchform.cleaned_data.get('author')
            bookisbn = book_searchform.cleaned_data.get('isbn')
            if booktitle:
                book = Book.objects.filter(title__contains=booktitle)
                messages.success(request, f'Here are your books that title name contains {booktitle}!')
                return render(request, 'home.html', context={'books': book, 'book_searchform': book_searchform})
            elif bookauthor:
                book = Book.objects.filter(author__contains=bookauthor)
                messages.success(request, f'Here are your books that author name contains {bookauthor} !')
                return render(request, 'home.html', context={'books': book, 'book_searchform': book_searchform})
            elif bookisbn:
                book = Book.objects.filter(isbn__exact=bookisbn)
                messages.success(request, f'Here are your books with ISBN number : {bookisbn}!')
                return render(request, 'home.html', context={'books': book, 'book_searchform': book_searchform})
            elif pub_date_from:
                if pub_date_to:
                    book = Book.objects.filter(publication_date__range=[pub_date_from, pub_date_to])
                    messages.success(request, f'Here are your books!Published from {pub_date_from} to {pub_date_to} ')
                    return render(request, 'home.html', context={'books': book, 'book_searchform': book_searchform})
                else:
                    book = Book.objects.filter(publication_date__gte=pub_date_from)
                    messages.success(request, f'Here are your books! Published from {pub_date_from}')
                    return render(request, 'home.html', context={'books': book, 'book_searchform': book_searchform})
            else:
                messages.warning(request,
                                 f'You dont give enough information or there is no such book in database!')
                return render(request, 'home.html',
                              context={'book_searchform': book_searchform})


class BookAddView(View):
    def get(self, request):
        """  Book add form"""
        book_addform = BookAddForm(request.POST)
        context = {
            #           'google_title': title,
            #            'google_author': author,
            #            'google_pages': pages,
            #            'google_isbn': isbn,
            #            'google_language': language,
            #            'google_cover': image,
            #            'google_publication_date': pub_date,
            'book_addform': book_addform}
        return render(request, 'bookadd.html', context=context)

    def post(self, request):
        book_addform = BookAddForm(request.POST)
        if book_addform.is_valid():
            book_addform.save()
            messages.success(request, f'Your book has been added!')
            return redirect('home')
        else:
            messages.warning(request, f'Something went wrong!')
            return redirect('home')


class GoogleBooks(View):
    def get(self, request, *args, **kwargs):
        form = SearchBookForm(request.POST)
        return render(request, 'import_book.html', {'form': form})

    def add_book_to_library(self, fetched_books):
        for book in fetched_books:
            Book.objects.get_or_create(
                title=book['volumeInfo']['title'],
                cover=book['volumeInfo']['imageLinks']['thumbnail'] if 'imageLinks' in book['volumeInfo'] else "",
                author=", ".join(book['volumeInfo']['authors']) if 'authors' in book['volumeInfo'] else "",
                publication_date=book['volumeInfo']['publishedDate'][0:3] if 'publishedDate' in book[
                    'volumeInfo'] else "",
                pages_nr=book['volumeInfo']['pageCount'] if 'pageCount' in book['volumeInfo'] else None,
                language=book['volumeInfo']['language'] if 'language' in book[
                    'volumeInfo'] else "",
                isbn=book['volumeInfo']['industryIdentifiers'] if 'industryIdentifiers' in book[
                    'volumeInfo'] else "",

            )

    def post(self, request, *args, **kwargs):
        form = SearchBookForm(request.POST)

        if form.is_valid():
            q = form.cleaned_data.get('q')
            maxResult = 15
            api_key = env.str('API_KEY')
            search_url = f'https://www.googleapis.com/books/v1/volumes?q={q}'
            params = {
                'key': api_key,
                'orderBy': 'relevance',
                'maxResults': maxResult,
            }
            data = requests.get(search_url, params=params).json()

            print(data)

        if not 'items' in data:
            return render(request, 'books.html', {'message': 'Sorry, no books match that search term.'})

        fetched_books = data['items']
        books = []
        for book in fetched_books:
            book_dict = {
                'title': book['volumeInfo']['title'],
                'image': book['volumeInfo']['imageLinks']['thumbnail'] if 'imageLinks' in book['volumeInfo'] else "",
                'authors': ", ".join(book['volumeInfo']['authors']) if 'authors' in book['volumeInfo'] else "",
                'publisher': book['volumeInfo']['publisher'] if 'publisher' in book['volumeInfo'] else "",
                'info': book['volumeInfo']['infoLink'] if 'infolink' in book['volumeInfo'] else "",
                'language': book['volumeInfo']['language'] if 'language' in book['volumeInfo'] else "",
                'isbn': book['volumeInfo']['industryIdentifiers'] if 'industryIdentifiers' in book[
                    'volumeInfo'] else "",
                'published_date': book['volumeInfo']['publishedDate'] if 'publishedDate' in book[
                    'volumeInfo'] else "",
                'pages': book['volumeInfo']['pageCount'] if 'pageCount' in book['volumeInfo'] else "",
            }
            books.append(book_dict)
            self.add_book_to_library(fetched_books)

        return render(request, 'books.html', {'books': books})


class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
