from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

association_table = db.Table("association", db.Model.metadata,
  db.Column("book_id", db.Integer, db.ForeignKey("book.id")),
  db.Column("author_id", db.Integer, db.ForeignKey("author.id")))

# Our project is a "mini-online library"
# Many-to-many relationship:A book can have multiple authors, and an author can have published multiple books
# One-to-many relationship: A book can have multiple reviews, but a revuew will only correspond to a book

class Book(db.Model):    
  __tablename__ = "book"    
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String, nullable=False)
  published_year = db.Column(db.String, nullable=False)
  authors = db.relationship("Author", secondary=association_table, back_populates="books")
  reviews = db.relationship("Review", cascade="delete")
  def serialize_book(self):
    return {            
      "id": self.id,
      "title": self.title,
      "published_year": self.published_year,
      "authors": [x.serialize_author() for x in self.authors],
      "reviews": [y.serialize_review() for y in self.reviews]
    }

  def serialize_book_short(self):
    return {            
      "id": self.id,
      "title": self.title,
      "published_year": self.published_year,
      "reviews": [x.serialize_review() for x in self.reviews]
    }

class Review(db.Model):    
  __tablename__ = "review"    
  id = db.Column(db.Integer, primary_key=True)
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
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  books = db.relationship("Book", secondary=association_table, back_populates='authors')
  def serialize_author(self):
    return {            
      "id": self.id,
      "name": self.name,
      "books": [x.serialize_book_short() for x in self.books]
    }