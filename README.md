# Book Recommender

I created a book recommender web application based on django framework.

In this app I used a book-genre dataset which has approximately 10k records with 215 genres. Each record is a book and multiple genres for it, alongside the author and the publication date. I used [this dataset](https://www.cs.cmu.edu/~dbamman/booksummaries.html).

In order to use the dataset properly, I created a script to extract the needed information and save it in the application database.

## Idea
User chooses the books they like in the list. There is a search bar in the page for users to find their favorite books easier. After that, they click on the button “Get Suggestions” and they redirect to a page in which the recommended books are listed with a score. The score indicates the level of similarities between the recommended books and the books which user liked.

## Implementation

Each book has multiple genres; For example, “Book 1” is “fiction”, “Drama”, and “Fantasy”. “Book 2” is “Music” and “Drama”. “Book 3” is “Drama” and “realism”. “Book 4” is “fiction”.

- Book 1: Fiction, Drama, fantasy

- Book 2: Music, Drama

- Book 3: Drama, Realism

- Book 4: Fiction

Suppose user selects Book 1 and 2 as their favorite books. Therefore, each genre from each book gets a point. Ultimately, we have:

- Drama: 2

- Fiction: 1

- Fantasy: 1

- Music: 1

Now we compute a score for all of the books in the database:

- Book 3: Drama (2) and Realism (0). Therefore, the score is 2.

- Book 4: Fiction (1). Therefore, the score is 1.

So, it is clear that Book 3 is more related to the user’s favorite books. Therefore, if we want to recommend only one book, we recommend Book 3 to the user.

In the application, we sort all of the books based on their score and recommend 20 books with higher scores to the user.

## How to Use

First, you need to install the requirements of the project with this command:
```bash
pip install -r requirements.txt
```

After that, you should run the script in order to update database from the dataset:
```bash
python manage.py migrate
python manage.py shell
```
```python
>> from script import save_books_in_database
>> save_books_in_database()
```

When the operation finished, you can run the application with this command:
```bash
python manage.py runserver 8000
```
Now the application is running on `127.0.0.1:8000`. Enjoy!
