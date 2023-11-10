from django.db import models


class Book(models.Model):
    title = models.CharField(null=False, max_length=100)
    author = models.CharField(null=False, max_length=100)
    published_date = models.DateField(null=False)
    summary = models.CharField(max_length=2500)

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title


class Genre(models.Model):
    title = models.CharField(primary_key=True, unique=True, null=False, max_length=100)

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title


class BookGenre(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
