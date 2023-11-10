from collections import defaultdict

from recommender.models import BookGenre


def get_recommended_books(selected_genres):
    scores = defaultdict(int)

    books_genres = BookGenre.objects.filter(genre__title__in=set(selected_genres.keys()))

    for book_genre in books_genres:
        scores[book_genre.book] += selected_genres[book_genre.genre.title]

    return dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
