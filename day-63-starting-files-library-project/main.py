from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import sqlalchemy as sa


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)

class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    book: Mapped[str] = mapped_column(unique=True)
    author: Mapped[str] = mapped_column()
    rating: Mapped[float] = mapped_column()

app = Flask(__name__)

all_books = []


@app.route('/')
def home():
    message = 'Library Empty'
    return render_template('index.html', books=all_books, msg=message)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        book = Book(
            book=request.form.get('name'),
            author=request.form.get('author'),
            rating=request.form.get('rating'),
        )
        db.session.add(book)
        db.session.commit()

        # all_books.append(book)
        # print(all_books)
    return render_template('add.html')


if __name__ == "__main__":
    # configure the SQLite database, relative to the app instance folder
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
    # initialize the app with the extension
    db.init_app(app)
    with app.app_context():
        db.create_all()
    # book = db.Table(
    #     "book",
    #     sa.Column("id", sa.ForeignKey(Book.id), primary_key=True),
    #     sa.Column("book", sa.ForeignKey(Book.id), unique=True),
    #     sa.Column("author", sa.ForeignKey(Book.id), nullable=False),
    #     sa.Column("rating", sa.ForeignKey(Book.id), nullable=False),
    # )
    app.run(debug=True)


