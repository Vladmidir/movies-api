from main import *
import random

movies_to_test = [
    Movie("1", "", "movie1", "description 1", "2019-08-21", 1, 1),
    Movie("4", "", "movie4", "description 4", "2020-09-22", 4, 4),
    Movie("3", "", "movie3", "description 3", "2020-09-21", 3, 3),
    Movie("2", "", "movie2", "description 2", "2020-08-21", 2, 2)
]

# populate the list
for i in range(1000):
    # generate random ratings
    rand_rating = round(random.uniform(0.0, 10.0), 3)
    rand_user_rating = random.randint(0, 100)
    # generate random date
    rand_year = random.randint(1800, 2023)
    rand_month = random.randint(1, 12)
    rand_day = random.randint(1, 28)
    rand_date = f'{rand_year:04}-{rand_month:02}-{rand_day:02}'
    # create and append the movie object
    movie = Movie(str(i), "", "", "", rand_date, rand_rating, rand_user_rating)
    movies_to_test.append(movie)


# man these tests are shit! They will always evaluate to TRUE
# I need to make separate test lists for every type of sorting
# track the order in title attribute, shuffle and compare titles after sorting.
def test_sort_movies() -> None:
    """Test sort_movies() function"""

    # test sort by rating
    sort_movies(movies_to_test, "rating", True)
    for i in range(len(movies_to_test) - 1):
        assert movies_to_test[i].rating <= movies_to_test[i + 1].rating

    # test sort by date
    random.shuffle(my_movies)
    sort_movies(movies_to_test, "date_released", True)
    for i in range(len(movies_to_test) - 1):
        assert movies_to_test[i].release_date <= \
               movies_to_test[i + 1].release_date

    # test sort by date descending
    random.shuffle(my_movies)
    sort_movies(movies_to_test, "date_released", False)
    for i in range(len(movies_to_test) - 1):
        assert movies_to_test[i].release_date >= movies_to_test[i + 1].release_date

    # test sort by user_rating ascending
    random.shuffle(my_movies)
    sort_movies(movies_to_test, "user_rating", True)
    for i in range(len(movies_to_test) - 1):
        assert movies_to_test[i].user_rating <= movies_to_test[i + 1].user_rating

    # test sort by user_rating descending
    random.shuffle(my_movies)
    sort_movies(movies_to_test, "user_rating", False)
    for i in range(len(movies_to_test) - 1):
        assert movies_to_test[i].user_rating >= movies_to_test[i + 1].user_rating
