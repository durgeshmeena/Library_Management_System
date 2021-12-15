from datetime import timedelta
import requests
from flask.json import jsonify
from wtforms.fields import form
from app import app
from flask import render_template, redirect, url_for, flash ,request, session
from .model import *
from .controlars import *
from mongoengine.errors import ValidationError, DoesNotExist


@app.route('/')
def home():
    return render_template('home.html')


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
                    return redirect( url_for('signup') )
            except DoesNotExist:
                flash('Email not registered!!', 'danger')
                return redirect( url_for('login') )


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
            form_password = form.password.data

            try:
                existing_user = Member.objects.get(email=form_email)
                flash('Email already registered!!', 'danger')
                return redirect( url_for('signup') )
            except DoesNotExist:
                user = Member(name=form_name, email=form_email, password=form_password, admin=False )
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
            return redirect( url_for('signup') )  
    
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
        print(books_data)
        return jsonify(books_data)

    return render_template('add-book.html')                 
