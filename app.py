from flask import Flask, make_response, jsonify, request
from flask_mongoengine import MongoEngine
import mongoengine as Me

app = Flask(__name__)

database_name = 'API'
mongodb_password = 'admin'
DB_URI = "mongodb+srv://dba:{}@cluster0.czbzn.mongodb.net/{}?retryWrites=true&w=majority".format(mongodb_password, database_name)
app.config["MONGODB_HOST"] = DB_URI

db = MongoEngine()
db.init_app(app)


class Book(Me.Document):
    book_id = Me.IntField()
    autor = Me.StringField()
    titulo = Me.StringField()
    texto = Me.StringField()

    def to_json(self):
        return {
            "book_id": self.book_id,
            "autor": self.autor,
            "titulo": self.titulo,
            "texto": self.texto
        }

@app.route('/api/db_populate', methods=['POST'])
def db_populate():
    book1 = Book(book_id=1,autor='Afonso S C Junior', titulo='Covid 19 - Pesadelo ou realidade', texto='Será que os brasileiros estão disponíveis a vencer essa guerra?...')
    book2 = Book(book_id=2, autor='Daniel Boom', titulo= 'Sociedade do pre-conceito', texto='Toda sociedade é definida por conceitos...')
    book1.save()
    book2.save()
    return make_response("", 201)
    

@app.route('/api/books', methods=['GET', 'POST'])
def api_books():
    if request.method == 'GET':
        books=[]
        for book in Book.objects:
            books.append(book)
        return make_response(jsonify(books), 200)
    elif request.method == "POST":
        content = request.json
        book = Book(book_id=content['book_id'],autor=content['autor'],titulo=content['titulo'],texto=content['texto'])
        book.save()
        return make_response(" ", 201)

@app.route('/api/books/<book_id>', methods=['GET', 'PUT', 'DELETE'])
def api_each_book(book_id):
    if request.method == "GET":
        book_obj = Book.objects(book_id=book_id).first()
        if book_obj:
            return make_response(jsonify(book_obj.to_json()), 200)
        else:
            return make_response (" ", 404)
    elif request.method == "PUT":
        content = request.json
        book_obj = Book.objects(book_id=book_id).first()
        book_obj.update(autor = content['autor'], texto = content['texto'], titulo = content['titulo'])
        return make_response(" ", 204)
    elif request.method == "DELETE":
        book_obj = Book.objects(book_id=book_id).first()
        book_obj.delete()
        return make_response (" ", 204)

if __name__ == '__main__':
    app.run()