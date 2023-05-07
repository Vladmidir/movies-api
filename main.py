from datetime import datetime

from typing import Optional
import requests
from flask import Flask, render_template, url_for, request, redirect
import json

# read the config file credentials
with open("config.json", "r") as jsonfile:
    data = json.load(jsonfile)

app = Flask(__name__)
# make a session
app.config['SECRET_KEY'] = data["SECRET_KEY"]

# Movie API url
url = "https://moviesminidatabase.p.rapidapi.com/movie"

headers = {
    "X-RapidAPI-Key": data["X-RapidAPI-Key"],
    "X-RapidAPI-Host": "moviesminidatabase.p.rapidapi.com"
}

# list of user selected movies. Do I really need this or can I get rid of it?
my_movies = []
# List of dicts {id: Movie}. Only includes the movies from my_movies
id_to_movie = {}


@app.route('/')
def index():
    # don't forget to set the headers!
    response = requests.get(f'{url}/order/byPopularity', headers=headers)
    movie_dict = response.json()['results']
    return render_template('index.html', movies=movie_dict)


# want to display status. Whether in the library or not.
@app.route('/id/<movie_id>')
def movie_page(movie_id):
    # this always get's data from the API. I want to show the data from
    # the my_movies list if the id is in the list. Rename Movie.id to imdb_id
    response = requests.get(f'{url}/id/{movie_id}/', headers=headers)
    movie = response.json()['results']
    if movie_in_list(movie['imdb_id'], my_movies):
        movie = id_to_movie[movie_id]
        return render_template('movie.html', movie=movie, in_list=True)
    else:
        return render_template('movie.html', movie=movie, in_list=False)


@app.post('/name/')
def list_by_name():
    movie_name = request.form['movie_name']
    response = requests.get(f'{url}/imdb_id/byTitle/{movie_name}',
                            headers=headers)
    movie_dict = response.json()['results']
    return render_template('search.html', movies=movie_dict,
                           movie_name=movie_name)


@app.post('/add/<movie_id>')
def add_movie(movie_id):
    response = requests.get(f'{url}/id/{movie_id}/', headers=headers)
    movie_json = response.json()['results']
    movie = make_movie(movie_json)
    my_movies.append(movie)
    id_to_movie[movie_id] = movie

    return redirect(url_for('movie_page', movie_id=movie_id))


@app.post('/delete/<movie_id>')
def delete_movie(movie_id):
    for movie in my_movies:
        if movie.id == movie_id:
            # delete all records
            my_movies.remove(movie)
            del id_to_movie[movie_id]
            # alert the user that the movie was removed
            break
    return redirect(url_for('movie_page', movie_id=movie_id))


@app.route('/edit/<movie_id>', methods=['GET', 'POST'])
def edit_movie(movie_id):
    if request.method == 'POST':
        form = request.form
        movie = id_to_movie[movie_id]
        movie.change_description(form['description'])
        movie.change_rating(int(form['user_rating']))

        return redirect(url_for('movie_page', movie_id=movie_id))
    else:
        return render_template('edit.html', movie=id_to_movie[movie_id])


@app.route('/list', methods=['POST', 'GET'])
def movies_list():
    # filter form was submitted. Filter the movies and re-render template
    if request.method == 'POST':
        form = request.form
        sort_movies(my_movies, form['sort_by'], bool(form['order']))
        return render_template('list.html', movies=my_movies)
    else:
        return render_template('list.html', movies=my_movies)


class Movie:
    """
    This represents a user-selected movie

    === Attributes ===
    id: unique identifier that maps the movie to the API.
    banner: link to the banner of the movie.
    title: name of the movie. Should not be changed.
    description: short summary of the movie.
    release_date: date the movie was released. Format: yyyy-mm-dd
    rating: IMDB rating.
    user_rating: user specified rating.
    sort_by: parameter by which the movies are compared to each other

    === Representation Invariants ===
    id: unique
    0 <= rating <= 10
    0 <= user_rating <= 100

    """
    id: str
    banner: str
    title: str
    description: str
    release_date: str
    rating: float
    user_rating: int
    sort_by: str

    def __init__(self, id: str, banner: str, title: str, description: str,
                 release_date: str, rating: float,
             user_rating: Optional[int] = 0) -> None:
        self.id = id
        self.banner = banner
        self.title = title
        self.description = description
        self.release_date = release_date
        self.rating = rating
        self.user_rating = user_rating
        self.sort_by = "rating" # sort by rating by default

    def __eq__(self, other):
        if self.sort_by == "rating":
            if self.rating == other.rating:
                return True
            return False
        elif self.sort_by == "user_rating":
            if self.user_rating == other.user_rating:
                return True
            return False
        else: # self.sort_by == "release_date"
            if self.release_date == other.release_date:
                return True
            return False

    def __gt__(self, other):
        if self.sort_by == "rating":
            if self.rating > other.rating:
                return True
            return False
        elif self.sort_by == "user_rating":
            if self.user_rating > other.user_rating:
                return True
            return False
        else: # self.sort_by == "release_date"
            # convert str to datetime.date
            # MAKE SURE THESE ARE THE RIGHT PARAMETERS!
            self_date = datetime.strptime(self.release_date, '%Y-%m-%d').date()
            other_date = datetime.strptime(other.release_date, '%Y-%m-%d').date()
            if self_date > other_date:
                return True
            return False

    def __lt__(self, other):
        return not self.__gt__(other)

    def __str__(self):
        return f'{self.title} released on {self.release_date}'

    def change_description(self, new_description: str) -> None:
        """Change the description attribute"""
        self.description = new_description

    def change_rating(self, new_rating: int) -> None:
        """Change the rating attribute"""
        self.user_rating = new_rating


def make_movie(data: dict) -> Movie:
    """Create Movie object."""
    id = data['imdb_id']
    banner = data['banner']
    title = data['title']
    description = data['description']
    release_date = data['release']
    rating = data['rating']

    return Movie(id, banner, title, description, release_date, rating)


def movie_in_list(id: str, lst: list) -> bool:
    """Return true if the movie with the given id is in the lst"""
    for movie in my_movies:
        if movie.id == id:
            return True
    return False


def sort_movies(movies: list[Movie], attribute: str, ascending: bool) -> None:
    """
    Sort the movies based on the attribute.
    Mutates my_movies list.
    """
    # read about custom sorting
    # here: https://learnpython.com/blog/python-custom-sort-function/
    # good new, my implementation does not spit error
    # bad news, it does not sort anything
    for movie in movies:
        movie.sort_by = attribute

    if ascending:
        movies.sort()
    else:
        movies.sort(reverse=True)
