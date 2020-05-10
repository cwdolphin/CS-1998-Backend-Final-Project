from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

association_table = db.Table("association", db.Model.metadata,
  db.Column("book_id", db.Integer, db.ForeignKey("book.id")),
  db.Column("author_id", db.Integer, db.ForeignKey("author.id")))

# Our project is a "mini-online library" that contains 4 tables: book, author, genre, and review
# Many-to-many relationship: A book can have multiple authors, and an author can have published multiple books
# One-to-many relationship: A book can have multiple reviews, but a review will only correspond to a book
#                           A book will only have a single genre, but a genre can correspond to multiple books

class Book(db.Model):    
  __tablename__ = "book"    
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  title = db.Column(db.String, nullable=False)
  published_year = db.Column(db.Integer, nullable=False)
  genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"), nullable=False)
  authors = db.relationship("Author", secondary=association_table, back_populates="books")
  reviews = db.relationship("Review", cascade="delete")
  def serialize_book(self):
    genre = Genre.query.filter_by(id=self.id).first()
    return {            
      "id": self.id,
      "title": self.title,
      "published_year": self.published_year,
      "genre": {"id": genre.id, "name": genre.name},
      "authors": [x.serialize_author() for x in self.authors],
      "reviews": [y.serialize_review() for y in self.reviews]
    }

  def serialize_book_short(self):
    genre = Genre.query.filter_by(id=self.id).first()
    return {            
      "id": self.id,
      "title": self.title,
      "published_year": self.published_year,
      "genre": {"id": genre.id, "name": genre.name},
      "reviews": [x.serialize_review() for x in self.reviews]
    }

class Genre(db.Model):
  __tablename__ = "genre" 
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  books = db.relationship("Book")
  def serialize_genre(self):
    return {            
      "id": self.id,
      "name": self.name,
      "books": [x.serialize_book_short() for x in self.books]
    }

class Review(db.Model):    
  __tablename__ = "review"    
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  content = db.Column(db.String, nullable=False)
  book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
  def serialize_review(self):
    book = Book.query.filter_by(id=self.id).first()
    return {            
      "id": self.id,
      "content": self.content,
      "book": {"id": book.id, "title": book.title, "published_year": book.published_year}
    }

class Author(db.Model):    
  __tablename__ = "author"    
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String, nullable=False)
  books = db.relationship("Book", secondary=association_table, back_populates='authors')
  def serialize_author(self):
    return {            
      "id": self.id,
      "name": self.name,
      "books": [x.serialize_book_short() for x in self.books]
    }