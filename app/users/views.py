from . import user_bp
from flask import render_template, redirect, request, url_for, make_response, session, flash
from datetime import timedelta, datetime

@user_bp.route("/profile")
def get_profile():
    if "username" in session:
        username_value = session["username"]
        color_theme = request.cookies.get('color_theme', 'light')
        cookies_data = request.cookies.items() 
    
        return render_template("profile.html", username=username_value, cookies=cookies_data, color_theme=color_theme)
    flash("Invalid session: You need to log in to access this page.", "danger")
    return redirect(url_for("users.login"))

@user_bp.route("/login" , methods=['GET', 'POST'])
def login():
    if "username" not in session:
      if request.method == "POST":
          username = request.form["username"].strip()
          password = request.form["password"].strip()
          if username == 'student' and password == 'studentPass':
            session["username"] = username
            flash("Success: You have successfully logged in.", "success")
            return redirect(url_for("users.get_profile"))
          else: 
              flash("Wrong data! Try again!", "danger")
      return render_template("login.html")
    return redirect(url_for("users.get_profile"))
@user_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('users.login'))


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