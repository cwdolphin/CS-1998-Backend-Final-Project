# CS-1998-Backend-Final-Project

## GET methods  

### /api/book/{id}/
  gets the corresponding book from {id} or returns a 'no book' response
### /api/genre/{id}/  
  gets the corresponding genre from {id} or returns a 'no genre' response
### /api/author/{id}/
  gets the corresponding author from {id} or returns a 'no author' response
### /api/book/
  gets all books
### /api/genre/
  gets all genres
### /api/author/
  gets all authors
### /api/reviews/
  gets all reviews
### /api/user/
  gets all users

## POST methods

### /api/register/
  creates a user with 'username' and 'password' from the body. Returns 'username exists' response if username exists
### /api/author/
  creates an author with 'name' from the body
### /api/book/{id}/review/
  creates a new review on the book {id} with 'content', 'username', and 'password'. Returns failure response if the user from 'username' and 'password' are invalid or if the {id} does not match to any book
### /api/genre/
  creates a new genre with 'name'
### /api/book/{id}/author/
  updates a book with {id} to an author with 'author_id'. Returns failure response if {id} does not match to a book or 'author_id' does not match to an author
### /api/genre/{id}/book/
  Creates a book to the genre with {id}. Returns failure response if {id} does not match to a genre.

## DELETE methods

### /api/book/{id}/
  Deletes the book with {id}. Returns failure response if {id} does not match to a book
