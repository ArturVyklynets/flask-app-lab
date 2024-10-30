from . import user_bp
from flask import render_template, redirect, request, url_for, make_response
from datetime import timedelta, datetime


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

@user_bp.route('/set_cookie')
def set_cookie():
    response = make_response('Кука встановлена')
    response.set_cookie('username', 'student', expires=datetime.now()+timedelta(seconds=10))
    response.set_cookie('username', 'student', max_age=timedelta(seconds=10))
    return response

@user_bp.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username')
    return f'Користувач: {username}'

@user_bp.route('/delete_cookie')
def delete_cookie():
    response = make_response('Кука видалена')
    response.set_cookie('username', '', expires=0) # response.set_cookie('username', '', max_age=0)
    return response