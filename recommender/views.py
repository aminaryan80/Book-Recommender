import json
from collections import defaultdict

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from recommender.models import Book, BookGenre
from recommender.utils import get_recommended_books


def index_view(request):
    books = Book.objects.order_by('title').all()
    return render(request, 'index.html', context={'books': books})


@csrf_exempt
def recommend_view(request):
    data = json.loads(request.POST['selectedBooks'])
    books = Book.objects.order_by('title').all()
    selected_books = list()
    selected_genres = defaultdict(int)
    for i, book in enumerate(books):
        if i in data:
            selected_books.append(book)

    for book in selected_books:
        genres = BookGenre.objects.filter(book=book).values_list('genre__title', flat=True)
        for genre in genres:
            selected_genres[genre] += 1

    recommended_books = get_recommended_books(selected_genres)

    recommended_books_with_scores = list()
    for recommended_book, score in recommended_books.items():
        recommended_books_with_scores.append(
            {
                'title': recommended_book.title,
                'author': recommended_book.author,
                'published_date': recommended_book.published_date,
                'score': score
            }
        )

    return render(request, 'recommender.html', context={'books': recommended_books_with_scores[:20]})
