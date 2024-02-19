from flask import Flask
from flask import request , render_template , url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from datetime import datetime
from sqlalchemy import func

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)




class Books(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    image = db.Column(db.String, nullable=True)
    price = db.Column(db.Integer)
    no_of_pages = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=func.now())


    def __str__(self):
        return f"{self.title}"




@app.route("/mybook", endpoint='books.index')
def books_index():
    # Query all books from the database
    bks = Books.query.all()
    # Render the template and pass the books data
    return render_template("books/index.html", bks=bks)



@app.route("/bookDetails/<int:id>", endpoint="mybook.details")
def bookDetails_show(id):
    bk=Books.query.get_or_404(id)
    return render_template("books/details.html" , bk=bk)    


@app.route("/mybook/createbook",methods=['GET','POST'],endpoint="book.create")
def create_book():
    if request.method == 'POST':
        title = request.form.get('title')
        image = request.form.get('image')
        price = request.form.get('price')
        no_of_pages = request.form.get('no_of_page')
        book = Books(title=title, image=image ,price=price ,no_of_pages=no_of_pages ) 
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('books.index'))
    return render_template("books/create.html")


@app.route('/update_book/<int:book_id>', methods=['GET', 'POST'], endpoint="book.update")
def update_book(book_id):
    # Get the book object from the database
    book = Books.query.get_or_404(book_id)

    if request.method == 'POST':
        try:
            # Update the book's information
            book.title = request.form['title']
            book.image = request.form['image']
            book.price = request.form['price']
            book.no_of_pages = request.form['no_of_pages']
            db.session.commit()
            return redirect(url_for('books.index'))
        except KeyError:
            return redirect(request.url)

    # Render the template with the book data
    return render_template("books/update.html", book=book)



@app.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    # Get the book object from the database
    book = Books.query.get_or_404(book_id)
    # Delete the book from the database
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('books.index'))



@app.errorhandler(404)
def get_404(error):
    return render_template("error404.html")



if __name__ == '__main__':
    app.run(debug=True)