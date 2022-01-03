import datetime
from werkzeug.security import  generate_password_hash, check_password_hash 

from mongoengine import (
    BooleanField, 
    DateTimeField, 
    DateField,
    Document, 
    FloatField,
    IntField,
    ListField, 
    ObjectIdField,
    ReferenceField ,
    StringField, 
    SequenceField,
)


# ========== Database Models ==============

class Book(Document):
    bookID = StringField()
    title = StringField()
    authors = StringField()
    average_rating = FloatField()
    isbn = StringField()
    isbn13 = StringField()
    language_code = StringField()
    num_pages = IntField()
    ratings_count = IntField()
    text_reviews_count = StringField()
    publication_date = StringField()
    publisher = StringField()

    stock = IntField(default=10)
    issue_count = IntField(default=0)
    available = BooleanField(default=True)



class Member(Document):
    name = StringField(max_length=50)
    email = StringField(required=True, max_length=20)
    username = StringField(required=True, max_length=20)
    password = StringField(max_length=255)
    admin = BooleanField(required=True, dafault=False)

    active = BooleanField(required=True, dafault=False)
    created_on = DateTimeField(default=datetime.datetime.now)

    current_book = ListField(ReferenceField(Book))
    issued_books = ListField(ReferenceField(Book))
    balance = FloatField(default=0.00)
    total_purchased = FloatField(default=0.0)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, form_password):
        return check_password_hash(self.password, form_password)

    def is_admin(self):
        return self.admin




class Transaction(Document):
    id = SequenceField(primary_key=True)
    member = StringField()
    book = StringField()
    borrow = BooleanField(required=True,default=True)
    date = DateTimeField(default=datetime.datetime.now)




