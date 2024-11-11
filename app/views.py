from flask import request,render_template
from . import app

@app.route('/')
def main():
  return render_template("base.html")

@app.route('/homepage') 
def home():
    """View for the Home page of your website."""
    agent = request.user_agent

    return render_template("home.html", agent=agent)

@app.errorhandler(404)
def page_not_found(error):
  return render_template('404.html'), 404

@app.route('/resume')
def resume():
  return render_template("resume.html")