### future development
do NOT add a database to this
- [x] on the homepage display popular movies. 
- [x] What I want is to make a session, that will save user preferences in temporary
python objects.
- [x] Make a list of user selected movies. Each movie will belong to the Movie class.
- [x] For now, I want to allow the user to search for a movie in the API database. Search
by name/ or search by category. I will have to add forms for this.
- [x] When a user searches for movie, they can add it to their list of movies.
- [x] Make a movie.html that display the movie.
- [x] The user can edit the description and change it to their own.
  - make an edit_movie POST route
- [ ] Ask for confirmation when deleting a movie.
- [x] The user can add their personal rating, that will NOT override the original.
  - Give Movie class an optional attribute user_rating. 
  - When open a movie page, check if it is in the list. 
  If it is, send the movie object from the list. 
  - Add an if statement to determine whether to render movie from API or 
  the Movie class object.
- [x] In the MyList section user should be able to view and sort their movies.
Sort by: rating, personal_rating, date. Ascending/descending.
  - Need to make a sorting algorith. Implement comparison functions for 
  the Movie class? Yes!
- [ ] Need to keep track of when the movie was added and sort in order added.
- [x] In the movie.html, the user should see whether the movie is a part of their
movie list. 
- [x] The user should be able to add/remove a movie from its page.

### General notes:
Try using Flask shell to debug. Should make it easier. 

To generate secret key:
```
>>> import os
>>> os.urandom(24).hex()
```
Flask url_for() method returns url for the view function!
