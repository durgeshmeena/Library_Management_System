from datetime import timedelta
from flask import json
import requests
from flask.json import jsonify
from app import app
from flask import render_template, redirect, url_for, flash ,request, session
from .model import *
from .controlars import *
from mongoengine.errors import DoesNotExist

@app.route('/')
def home():
    return render_template('home.html')

@app.errorhandler(404) 
def invalid_route(e): 
    return render_template('404.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()


    if request.method=='POST' :
        
        # ========== Form Validation ===========
        print('validate?: ', form.validate() )
        print('errors: ', form.email.errors, form.password.errors)

        if form.validate():
 
            print('this worked')
            # ==========  User validation =============
            form_email = form.email.data
            form_email = form_email.lower()
            form_password = form.password.data
            form_checkbox = form.checkbox.data

            try:
                user = Member.objects.get(email=form_email)
                if user.check_password(form_password):
                    flash('User Data correct', 'success')

                    session.permanent = True
                    if form_checkbox:
                        app.permanent_session_lifetime = timedelta(days=1)
                    else:
                        app.permanent_session_lifetime = timedelta(hours=1)
                    session['user'] = user
                    session['logged_in'] = True

                    return jsonify(user)

                else:
                    flash('Password is incorrect', 'danger')
                    return redirect( url_for('login') )
            except DoesNotExist:
                flash('Email not registered!!', 'danger')
                return redirect( url_for('signup') )


        else:
            if form.email.data == '':
                flash('Email is required', 'danger')
            else:    
                flash_errors(form)
            return redirect( url_for('login') )  
    
    return render_template('login.html', form=form)    

    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method=='POST' :
        # ========== Form Validation ===========
        # print('validate?: ', form.validate() )
        # print('errors: ', form.email.errors, form.password.errors)

        if form.validate():
            print('this worked')
            # ==========  User validation =============
            form_name = form.name.data
            form_email = form.email.data
            form_email = form_email.lower()
            form_username = form.username.data
            form_password = form.password.data

            try:
                existing_email = Member.objects.get(email=form_email)

                flash('Email already registered!!', 'danger')
                # return redirect( url_for('signup') )
            except DoesNotExist:
                try:
                    existing_user = Member.objects.get(username=form_username)
                    flash('Username already registered!!', 'danger')
                    # return redirect( url_for('signup') )

                except DoesNotExist:
                    
                    user = Member(name=form_name, email=form_email, password=form_password,username=form_username, admin=False,active=False )
                    user.set_password(form_password)
                    user.save()
                    return jsonify(user), 200
                
            
            # return redirect( url_for('signup') )  

        else:
            if form.name.data == '':
                flash('Name is required', 'danger')
            elif form.email.data == '':
                flash('Email is required', 'danger')
            else:    
                flash_errors(form)
            
            # return render_template('signup.html', form=form)
            # return redirect( url_for('signup') )
                
    
    return render_template('signup.html', form=form)    


@app.route('/dashboard/')
# @login_required
def dashboard():
    return render_template('dashboard.html')
                 
@app.route('/add-book', methods=['GET', 'POST'])
def add_book():
    if request.method=='POST':
        title = request.form.get('title')
        author = request.form.get('author')
        isbn = request.form.get('isbn')
        publisher = request.form.get('publisher')
        page = request.form.get('page')

        frappe_api_url = 'https://frappe.io/api/method/frappe-library?'

        for key, value in request.form.items():
            if value:
                frappe_api_url = frappe_api_url + key + '=' + value + '&'
        request_url = frappe_api_url[:-1]

        print(request_url)
        books_req = requests.get(request_url).json()
        books_data = books_req.get('message')
        # print(books_data)
        for book in books_data:
           
            db_book = Book.objects(bookID=(book['bookID']))
            # print(db_book)
            if len(db_book) == 0:
                new_book = Book(bookID=book['bookID'],title=book['title'],
                authors=book['authors'],average_rating=book['average_rating'],
                isbn=book['isbn'],isbn13=book['isbn13'],language_code=book['language_code'],
                num_pages=book["  num_pages"],ratings_count=book['ratings_count'],text_reviews_count=book['text_reviews_count'],
                publication_date=book['publication_date'],publisher=book['publisher'])
                # print(new_book)
                new_book.save()
                flash('book added successfully','success')
            else:
                flash('Book Already Exist', 'danger')

        # return jsonify(books_data)

    return render_template('add-book.html')                 


@app.route('/books')
def books():
    books = Book.objects()
    members=Member.objects()
    return render_template('books2.html',books=books,members=members)

@app.route('/members')
def members():
    print("Reached1")
    members = Member.objects()
       
    return render_template('members.html',members=members)



@app.route('/member/<username>')
def member(username):
    
    # print("Reached1")
    member = Member.objects(username=username)
    if len(member) > 0:
        member = member[0]

       
    return render_template('member.html',member=member)





@app.route('/modal')
def modal():
    return render_template('modal.html')

@app.route('/member/<id>',methods=['POST'])
def modify(id):
    member=Member.objects(pk=id)
    print(member)
    print(request.form)
    update_name=request.form['name']
    update_email=request.form['email']
    update_balance=request.form['balance']
    update_active=request.form.get('active')

    if update_active:
        update_active=True
    else:
        update_active=False
    # print(update_email)
    # print(member[0]['email'])

    if update_email == member[0]['email']:
        updated_member=Member.objects(id=id).update(set__name=update_name,set__balance=update_balance,set__active=update_active)
        # member[0]['name']=update_name
        # member[0]['balance']=update_balance
        # member[0]['active']=update_active
        # member[0].save()
        print(updated_member)
        flash('Data Updated Successfully','success')

    else:
        flash('Oops! Unable to Save Data','Danger')
    print(request.form)

    url       =   member[0]['username']
    return redirect(url)
    # return redirect(url_for('members'))











@app.route('/<name>/remove/<id>',methods=['POST'])
def remove(name,id):
    if name == 'members':
        user = Member.objects(id=id)
        if user[0]['admin']:
            flash('Cannot Remove admin','danger')
            return {'name':'members','message':'Cannot Remove admin'}
        else:
            deleted_data=user[0].delete()
            flash('User Deleted SuccessFully','danger')
            return {'name':'members','message':'user deleted successfully'}

    elif name=='books':
        deleted_data=Book.objects(id=id).delete()
        flash('Book Deleted SuccessFully','danger')
        return {'name':'books','message':'book deleted successfully'}





@app.route('/books/modify/<id>',methods=['POST'])
def modify_book(id):
    data=request.form
    print(data) 
    quantity = request.form.get('quantity')
    available = request.form.get('active')
    print('available1=', available)
    if available:
        available = True
    else:
        available = False
            
    print('available2=', available)
    
    book = Book.objects(id=id)[0]
    book.update(set__stock=quantity, set__available=available)
        
    
    flash('Book Data Modified Sucessfully','success')
    return redirect(url_for('books'))

@app.route('/book/rent-out/<id>',methods=['POST'])
def rent_book(id):

    data = request.get_data().decode('utf-8')
    data = json.loads(data)

    print(data['user'], id)    
    
    user_email = data['user']
    member = Member.objects(email=user_email)
    print(member, bool(member))
    if member:
        member = member[0]
        book = Book.objects(id=id)[0]
        stock = book['stock']
        available = book['available']
        if stock>1:
            issue_count = book['issue_count'] +1
            stock = stock -1

            if stock==0:
                available = False
            book.update(set__issue_count=issue_count, set__stock=stock,set__available=available)
            
            member.update(add_to_set__current_book=[id])
            transaction = Transaction(book=book['title'],member=member['name'],borrow=True)
            transaction.save()
            flash('Book Issued Successfully','success')
        else:
            flash('Book Cannot be Issued','danger')
    else:
        flash('User not found','danger')

    return {'status':'Success'}
    

@app.route('/book/return', methods=['POST'])
def book_return():
    data = request.get_data().decode('utf-8')
    data = json.loads(data)

    user = data['user']
    book_name = data['book']
    book_id = data['id']

    # print(book_id, type(book_id))
    
    book_db = Book.objects(id=book_id).first()
    book_db_id = book_db['id']

    # print(book_db_id, type(book_db_id))

    member = Member.objects(username=user)[0]
    member.update( pull__current_book = book_db_id, add_to_set__issued_books=[book_db_id])

    transaction = Transaction(book=book_name,member=member['name'],borrow=False)
    transaction.save()
    
    flash('Book Returned Successfully','success')

    return {'username':user}


@app.route('/transactions')
def transactions():
    transactions = Transaction.objects()
    return render_template('transactions.html',transactions=transactions)


