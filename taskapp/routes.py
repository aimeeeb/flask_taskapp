# Project: Task App (CPSC 408 Final)
# 
# Created by Aimee Bowen
# Student ID: 2277842
# Email: bowen126@mail.chapman.edu
# Description: This file uses flask to generate each page and calls the functions needed per page.


from flask import render_template, url_for, flash, redirect, request, abort, send_from_directory
from taskapp import app, bcrypt, db_connection, db_cursor, datafunctions
from taskapp.forms import RegistrationForm, LoginForm, ListForm, TaskForm, EventForm
from flask_login import login_user, current_user, logout_user, login_required
import sys


@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    # get lists for current user
    posts = datafunctions.get_lists(current_user.get_id())
    return render_template('home.html', posts=posts)


@app.route("/list/<int:list_id>/task/new", methods=['GET','POST'])
def new_task(list_id):
    form = TaskForm()
    if form.validate_on_submit():
        # if valid inputs, add task to database
        datafunctions.create_task(form.title.data, form.date.data, form.description.data, list_id)
        flash(f'Your task has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_task.html', title="New Task", form=form, legend="New Task")

# creating csv for one list
@app.route("/list/<int:list_id>/csv")
def create_csv(list_id):
    file_dict = datafunctions.create_list_csv(list_id)
    dir = file_dict["path"]
    filename = file_dict["filename"]
    return send_from_directory(dir, filename, as_attachment=True)

# creating csv for all user's lists
@app.route("/account/csv")
def create_alltasks_csv():
    file_dict = datafunctions.create_alltasks_csv(current_user.get_id())
    dir = file_dict["path"]
    filename = file_dict["filename"]
    return send_from_directory(dir, filename, as_attachment=True)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db_cursor.execute("INSERT INTO Users(Username, Email, Password) VALUES (%s, %s, %s)",
                          (form.username.data, form.email.data, hashed_password))
        db_connection.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        # get user id
        db_cursor.execute("SELECT MAX(UserId) FROM Users WHERE Email = %s", (form.email.data,))
        user_id = db_cursor.fetchone()[0]
        if user_id:
            # if user id is in the database, get password
            db_cursor.execute("SELECT MAX(Password) FROM Users WHERE UserId = %s", (user_id,))
            user_password = db_cursor.fetchone()[0]
            # if password entered is valid
            if bcrypt.check_password_hash(user_password, form.password.data):
                user = datafunctions.load_user(user_id)
                # if user is not deleted
                if user:
                    login_user(user, remember=form.remember.data)
                    next_page = request.args.get('next')
                    return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/account")
@login_required
def account():
    task_count = datafunctions.count_tasks(current_user.get_id())
    list_count = datafunctions.count_lists(current_user.get_id())
    return render_template('account.html', task_count=task_count, list_count=list_count)


@app.route("/list/new",  methods=['GET', 'POST'])
@login_required
def new_list():
    form = ListForm()
    if form.validate_on_submit():
        datafunctions.create_list(form.title.data, form.date.data, current_user.get_id())
        flash(f'Your list has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_list.html', title="New List", form=form, legend="New List")


@app.route("/list/<int:list_id>/update",  methods=['GET', 'POST'])
@login_required
def update_list(list_id):
    this_list = datafunctions.get_list(list_id)
    if not this_list:
        abort(404)
    form = ListForm()
    if form.validate_on_submit():
        datafunctions.update_list(form.title.data, form.date.data, list_id)
        flash('Your list has been updated!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.title.data = this_list["title"]
    return render_template('create_list.html', title="Update List", form=form, legend="Update List")


@app.route("/list/<int:list_id>/delete", methods=['POST'])
@login_required
def delete_list(list_id):
    datafunctions.delete_list(list_id)
    flash('Your list has been updated!', 'success')
    return redirect(url_for('home'))


@app.route('/calendar')
def calendar():
    return render_template("json.html")


@app.route('/data')
def return_data():
    data = datafunctions.calendar_json(current_user.get_id())
    return data

@app.route("/event/new",  methods=['GET', 'POST'])
@login_required
def new_event():
    form = EventForm()
    if form.validate_on_submit():
        datafunctions.create_event(form.title.data, form.date.data, current_user.get_id())
        flash(f'Your event has been created!', 'success')
        return redirect(url_for('calendar'))
    return render_template('create_event.html', title="New Event", form=form, legend="New Event")
