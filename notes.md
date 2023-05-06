### future development
do NOT add a database to this
- [ ] Fix the data leak!
- [x] on the homepage display popular movies. 
- [ ] What I want is to make a session, that will save user preferences in temporary
python objects.
- [ ] Make a list of user selected movies. Each movie will belong to the Movie class.
- [x] For now, I want to allow the user to search for a movie in the API database. Search
by name/ or search by category. I will have to add forms for this.
- [ ] When a user searches for movie, they can add it to their list of movies.
- [x] Make a movie.html that display the movie.
- [ ] The user can edit the description and change it to their own.
The user can add their personal rating, that will NOT override the original.
- [ ] In the MyList section user should be able to view and sort their movies.
Sort by: rating, personal_rating, date. Ascending/descending.

### General notes:
To generate secret key:
```
>>> import os
>>> os.urandom(24).hex()
```
Flask url_for() method returns url for the view function!
