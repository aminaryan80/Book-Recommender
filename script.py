import re
from collections import defaultdict
from datetime import datetime

from recommender.models import Book, Genre, BookGenre


def _normalize_date(input_date):
    try:
        date_object = datetime.strptime(input_date, '%Y-%m-%d')
    except ValueError:
        try:
            date_object = datetime.strptime(input_date, '%Y-%m')
        except ValueError:
            try:
                date_object = datetime.strptime(input_date, '%Y')
            except ValueError:
                return 'Invalid date format'

    normalized_date = date_object.strftime('%Y-%m-%d')

    return normalized_date


def _extract_books_data():
    books = list()
    all_genres = set()

    with open('booksummaries.txt', 'r', encoding='utf-8') as file:
        line = file.readline()
        while line:
            row = re.match('(\d+)\t\/m\/[^\s]+\t([^\t]+)\t([^\t]+)\t([^\t]+)\t([^\t]+)\t([^\t\n]+)\n', line)
            if row is None:
                line = file.readline()
                continue
            title = row.group(2)
            author = row.group(3)
            date = row.group(4)
            date = _normalize_date(date)
            genres = set()
            for genre in re.findall('"[^\"]+": "([^"]+)"', row.group(5)):
                genres.add(genre)
            all_genres = all_genres | genres
            summary = row.group(6)
            books.append((title, author, date, genres, summary))
            line = file.readline()

    result = defaultdict(int)
    for book in books:
        for genre in book[3]:
            result[genre] += 1

    return books, all_genres


def save_books_in_database():
    books, genres = _extract_books_data()

    books_to_create = [
        Book(title=book[0], author=book[1], published_date=book[2], summary=book[4])
        for book in books
    ]

    genres_to_create = [
        Genre(title=genre)
        for genre in genres
    ]

    Book.objects.bulk_create(books_to_create)
    Genre.objects.bulk_create(genres_to_create)

    book_genres_to_create = list()

    books_objects = Book.objects.all()
    books_dict = dict()
    for book in books_objects:
        books_dict[book.title] = book

    genres_objects = Genre.objects.all()
    genres_dict = dict()
    for genre in genres_objects:
        genres_dict[genre.title] = genre

    for book in books:
        for genre in book[3]:
            book_genres_to_create += [BookGenre(book=books_dict[book[0]], genre=genres_dict[genre])]

    BookGenre.objects.bulk_create(book_genres_to_create)
