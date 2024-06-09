from flask import Flask
from flask_sqlalchemy import SQLAlchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

class Base(DeclarativeBase):
  pass

db = sa(model_class=Base)

app = Flask(__name__)

class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    book: Mapped[str] = mapped_column(unique=True)
    author: Mapped[str] = mapped_column()
    rating: Mapped[float]

if __name__ == '__main__':
    # configure the SQLite database, relative to the app instance folder
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
    # initialize the app with the extension
    db.init_app(app)
    with app.app_context():
        db.create_all()
    book = db.Table(
        "book",
        sa.Column("id", sa.ForeignKey(Book.id), primary_key=True),
        sa.Column("book", sa.ForeignKey(Book.id), unique=True),
        sa.Column("author", sa.ForeignKey(Book.id), nullable=False),
        sa.Column("rating", sa.ForeignKey(Book.id), nullable=False),
    )