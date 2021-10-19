"""googlebooksearch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from googlebooksearch_app.views import HomeView, BookAddView, GoogleBooks, BookListView, BookView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name="home"),
    # path('api/', BookGoogleApi.as_view(), name="api"),
    path('add/', BookAddView.as_view(), name="bookadd"),
    path('googlebooks/', GoogleBooks.as_view(), name="import_books"),
    path('books/', BookListView.as_view(), name='google_books'),
    path('books/<int:pk>/', BookView.as_view()),

]
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()