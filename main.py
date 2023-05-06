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

# list of user selected movies
my_movies = []


@app.route('/')
def index():
    # don't forget to set the headers!
    response = requests.get(f'{url}/order/byPopularity', headers=headers)
    movie_dict = response.json()['results']
    return render_template('index.html', movies=movie_dict)


# want to display status. Whether in the library or not.
@app.route('/id/<movie_id>')
def movie_page(movie_id):
    response = requests.get(f'{url}/id/{movie_id}/', headers=headers)
    movie = response.json()['results']
    return render_template('movie.html', movie=movie)


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

    return redirect(url_for('movie_page', movie_id=movie_id))


@app.route('/list')
def movies_list():
    return render_template('list.html', movies=my_movies)


# Should I store unchangeable attributes locally or just use the id for access?
class Movie:
    """
    This represents a user-selected movie

    === Attributes ===
    id: unique identifier that maps the movie to the API
    banner: link to the banner of the movie
    title: name of the movie. Should not be changed.
    description: short summary of the movie.
    rating: user specified rating.
    release_date: date the movie was released.

    === Representation Invariants ===
    id: unique
    0 <= custom_rating <= 10

    """
    id: str
    banner: str
    title: str
    description: str
    custom_rating: float
    release_date: str

    def __init__(self, id: str, banner: str, title: str, description: str,
                 release_date: str, rating: Optional[float] = 0) -> None:
        self.id = id
        self.banner = banner
        self.title = title
        self.description = description
        self.rating = rating
        self.release_date = release_date

    def change_description(self, new_description: str) -> None:
        """Change the description attribute"""
        self.description = new_description

    def change_rating(self, new_rating: int) -> None:
        """Change the rating attribute"""
        self.custom_rating = new_rating


def make_movie(data: dict) -> Movie:
    """Create Movie object."""
    id = data['imdb_id']
    banner = data['banner']
    title = data['title']
    description = data['description']
    release_date = data['release']
    rating = data['rating']

    return Movie(id, banner, title, description, release_date, rating)
