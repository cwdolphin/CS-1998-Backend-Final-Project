from db import db, Book, Author, Review, association_table

def add_book(book_title, book_published_year):
  new_book = Book(title = book_title, published_year = book_published_year)
  db.session.add(new_book)
  db.session.commit()
  return new_book.serialize_book()

def delete_book(book_id):
  delete_book = Book.query.filter_by(id=book_id).first()
  if delete_book is None:
      return None
  db.session.delete(delete_book)
  db.session.commit()
  return delete_book.serialize_book()

def create_author(author_name):
  new_author = Author(name = author_name)
  db.session.add(new_author)
  db.session.commit()
  return new_author.serialize_author()

def get_author(author_id):
  author = Author.query.filter_by(id=author_id).first()
  if author is None:
    return None
  return author.serialize_author()

def update_book_with_new_author(author_id, book_id):
  author = Author.query.filter_by(id=author_id).first()
  book = Book.query.filter_by(id=book_id).first()
  if author is None or book is None:
    return None
  book.authors.append(author)
  db.session.commit()
  return book.serialize_book()

def create_review(review_text, review_book_id):
  book = Book.query.filter_by(id=review_book_id).first()
  if book is None:
    return None
  new_reivew = Review(content = review_text, book_id = review_book_id)
  db.session.add(new_reivew)
  db.session.commit()
  return new_reivew.serialize_review()