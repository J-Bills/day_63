from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import sqlalchemy as sa


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)

class Book(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    author: Mapped[str] = mapped_column(nullable=False)
    rating: Mapped[float] = mapped_column(nullable=False)

app = Flask(__name__)

# all_books = []


@app.route('/')
def home():
    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result.scalars().all()
    return render_template('index.html', books=all_books)
@app.route('/book', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        with app.app_context():
            # Update Record
            book_id = request.form["id"]
            # print(book_id)
            book_to_update = db.get_or_404(Book, book_id)
            book_to_update.rating = request.form["rating"]
            db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = db.get_or_404(Book, book_id)
    return render_template("edit.html", book=book_selected)

@app.route('/remove', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        with app.app_context():
            book_id = request.form.get('id')
            book_to_delete = db.get_or_404(Book, book_id)
            db.session.delete(book_to_delete)
            db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_to_delete = db.get_or_404(Book, book_id)
    return render_template("delete.html", book=book_to_delete)

@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        book = Book(
            title=request.form.get('name'),
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

        # ##Creating a record##
        # new_book = Book(id=2,title="Harry Potter", author="J. K. Rowling", rating=9.3)
        # db.session.add(new_book)
        # db.session.commit()
        # ## Reading Records##
        # result = db.session.execute(db.select(Book).order_by(Book.title))
        # all_books = result.scalars().all()
        # print(all_books)
        # ##Updating Records##
        # book_to_update = db.session.execute(db.select(Book).where(Book.title == "Harry Potter")).scalar()
        # book_to_update.title = "Harry Potter and the Chamber of Secrets"
        # db.session.commit()
        # ##Updating record by Primary Key##
        # book_id = 2
        # book_to_update = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
        # # or book_to_update = db.get_or_404(Book, book_id)
        # book_to_update.title = "Harry Potter and the Goblet of Fire"
        # db.session.commit()
        # ## Deleting a record by Primary Key
        # book_id = 2
        #
        # book_to_delete = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
        # # or book_to_delete = db.get_or_404(Book, book_id)
        # db.session.delete(book_to_delete)
        # db.session.commit()

    app.run(debug=True)


