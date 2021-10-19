from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.
class Book(models.Model):
    """  Model of Book objects """
    title = models.CharField(max_length=512, blank=True)
    author = models.CharField(max_length=512, blank=True)
    publication_date = models.PositiveSmallIntegerField(validators=[MaxValueValidator(3000)],blank=True,null=True)
    language = models.CharField(max_length=512, blank=True)
    isbn = models.CharField(max_length=512, blank=True)
    cover = models.CharField(max_length=512, blank=True)
    pages_nr = models.IntegerField(blank=True, null=True)  # <- number of pages in a book

    def __str__(self):
        return f'{self.title} by {self.author}'
