import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from mysite import app, db, bcrypt
from mysite.models import usages, WorkUnit, Employee, User, Application
from mysite.forms import LoginForm, RegisterForm, UpdateAccountForm, ApplicationForm
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
def index():
    apks = Application.query.all()
    return render_template('index.html', apks=apks)

@app.route('/about')
def about():
    return render_template('about.html', title="About")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check username and password!', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route('/apk/new', methods=['GET', 'POST'])
@login_required
def new_apk():
    form = ApplicationForm()
    if form.validate_on_submit():
        apk = Application(
            name=form.name.data, description=form.description.data, status=form.status.data,
            platform=form.platform.data, database=form.database.data, user_id=current_user.id)
        db.session.add(apk)
        db.session.commit()
        flash('New appplication has been added!', 'success')
        return redirect(url_for('index'))
    return render_template('add_apk.html', title='New Application',
                           form=form, legend='New Application')


@app.route('/apk/<int:apk_id>')
def apk(apk_id):
    apk = Application.query.get_or_404(apk_id)
    return render_template('apk.html', title='Application', apk=apk)


@app.route('/apk/<int:apk_id>/update', methods=['GET', 'POST'])
@login_required
def update_apk(apk_id):
    apk = Application.query.get_or_404(apk_id)
    if current_user.username != 'ADMIN':
        abort(403)
    form = ApplicationForm()
    if form.validate_on_submit():
        apk.name = form.name.data
        apk.description = form.description.data
        apk.status = form.status.data
        apk.platform = form.platform.data
        apk.database = form.database.data
        db.session.commit()
        flash('This application has been updated!', 'success')
        return redirect(url_for('apk', apk_id=apk.id))
    elif request.method == 'GET':
        form.name.data = apk.name
        form.description.data = apk.description
        form.status.data = apk.status
        form.platform.data = apk.platform
        form.database.data = apk.database
    return render_template('add_apk.html', title='Update Application',
                           form=form, legend='Update Application')
