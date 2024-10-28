from . import user_bp
from flask import render_template, redirect, url_for, render_template, request

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
