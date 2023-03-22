from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)



class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80), unique=True, nullable=False)
    publisher= db.Column(db.String(70),unique=True, nullable=False)
    
    def __repr__(self):
        return f"{self.book_name} - {self.author}"
    
@app.route('/')
def index():
    return "Hello"   
@app.route('/books')
def get_books():
    books = Book.query.all()
    
    output =[]
    for book in books:
        book_data = {'Book name' :book.book_name, 'Author': book.author, "Publisher": book.publisher }
        
        output.append(book_data)
    return {"Books": output}

@app.route('/books/<id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return {"Book name": book.Book_name, "Author": book.author, "Publisher": book.publisher}

@app.route( '/books', methods=['POST'])
def add_book():
    book= Book(book_name=request.json['Book'], author=request.json["Author"])
    db.session.add(book)
    db.session.commit()
    return{'id: book.id'}

@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return {"error": "not found"}
    db.session.delete(book)
    db.session.commit()
    return{"message":"yeet@"}
