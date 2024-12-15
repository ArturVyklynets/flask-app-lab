from .models import User
from .forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_login import login_user, logout_user, current_user, login_required
from . import user_bp
from flask import render_template, redirect, request, url_for, make_response, session, flash
from datetime import timedelta, datetime
import os
from flask import current_app
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from app import db

@user_bp.route("/profile")
def get_profile():
    if current_user.is_authenticated:
        username_value = current_user.username
        color_theme = request.cookies.get('color_theme', 'light')
        cookies_data = request.cookies.items() 
    
        return render_template("profile.html", username=username_value, cookies=cookies_data, color_theme=color_theme)
    flash("Invalid session: You need to log in to access this page.", "danger")
    return redirect(url_for("users.login"))

@user_bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for(".get_account"))
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = User.hash_password(form.password.data)
        new_user = User(
            username=username,
            email=email,
            password=password,
        )        
        db.session.add(new_user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('.login'))
    return render_template('register.html', form=form, title='Register')

@user_bp.route("/login" , methods=['GET', 'POST'])
def login():
      if current_user.is_authenticated:
        return redirect(url_for(".get_account"))
      form = LoginForm()
      if form.validate_on_submit():
          email = form.email.data
          password = form.password.data
          user = User.query.filter_by(email=email).first()
          remember = form.remember.data
          if user and user.check_password(password):
              login_user(user, remember=remember)
              flash("Success: You have successfully logged in.", "success")
              return redirect(url_for(".get_account"))
          else: 
              flash("Wrong data! Try again!", "danger")
      return render_template("login.html", form=form, title="Login")

@user_bp.route('/account', methods=['GET', 'POST'])
@login_required
def get_account():
    local_time = datetime.utcnow() + timedelta(hours=2)
    current_user.last_seen = local_time
    db.session.commit()
    return render_template("account.html", title="Account", user=current_user)

@user_bp.route('/edit_account/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_account(id):
    user = db.get_or_404(User, id)
    form = UpdateAccountForm(obj=user)
    if form.validate_on_submit():
        # username
        user.username = form.username.data

        # check_email
        if form.email.data != user.email:
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user:
                flash("Email is already registered.", "danger")
                return redirect(url_for('.edit_account', id=user.id))
            else:
                user.email = form.email.data

        # about_me 
        user.about_me = form.about_me.data

        # image
        file = form.image_file.data
        if file:
          if isinstance(file, FileStorage): 
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            user.image_file = filename
          else:
            flash("No file selected!", "danger")

        # passwords
        if form.new_password.data and form.old_password.data and form.confirm_password.data:
          if form.old_password.data and user.check_password(form.old_password.data):
              if form.old_password.data != form.new_password.data:
                  if len(form.new_password.data) > 5:
                    user.password = User.hash_password(form.new_password.data)
                  else: 
                      flash("New password must be at least 6 characters.", "danger")
                      return redirect(url_for('.edit_account', id=user.id))
              else:
                  flash("New password is the same as old.", "danger")
                  return redirect(url_for('.edit_account', id=user.id))
          else:
              flash("Old password is incorrect.", "danger")
              return redirect(url_for('.edit_account', id=user.id))

        db.session.commit()
        flash(f'Account updated successfully!', 'success')
        return redirect(url_for('.get_account'))
    
    elif form.errors:
        flash(f"Enter the correct data in the form!", "danger")
    return render_template("edit_account.html", title="Edit Account", form=form, edit=True)

@user_bp.route('/users')
@login_required
def get_all_registered_users():
    users = User.query.all()
    return render_template('users_list.html', users=users, count=len(users))

@user_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('.login'))


@user_bp.route("/<string:name>")
def greetings(name):
   name = name.upper()
   age = request.args.get("age", None, int)
   return render_template("hi.html", name=name, age=age)

@user_bp.route("/admin")
def admin():
   to_url = url_for("users.greetings", name="administrator", age=45, _external=True)
   print(to_url)
   return redirect(to_url)

@user_bp.route('/set_cookie', methods=['GET', 'POST'])
def set_cookie():
    key = request.form.get('keyCookie')
    value = request.form.get('valueCookie')
    time = request.form.get('timeCookie')
    time = int(time)
    response = make_response(redirect(url_for('users.get_profile')))
    response.set_cookie( key, value, max_age=timedelta(seconds=time))
    return response

@user_bp.route('/get_cookie')
def get_cookie():
    cookies_data = request.cookies.items() 
    
    return render_template('profile.html', cookies=cookies_data)

@user_bp.route('/delete_cookie_by_key', methods=['GET', 'POST'])
def delete_cookie_by_key():
    key = request.form.get('keyCookie')
    response = make_response(redirect(url_for('users.get_profile')))
    response.set_cookie(key, '', expires=0)
    return response

@user_bp.route('/delete_all_cookies', methods=['GET', 'POST'])
def delete_all_cookies():
    response = make_response(redirect(url_for('users.get_profile')))
    for cookie in request.cookies:
        response.set_cookie(cookie, '', expires=0)
    return response

@user_bp.route('/profile/set_color_theme/<string:color>')
def set_color_theme(color):
    if color not in ['light', 'dark']:
        color = 'light'
    response = make_response(redirect(url_for('users.get_profile')))
    response.set_cookie('color_theme', color)
    return response