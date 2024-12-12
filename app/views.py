from flask import request,render_template, current_app 


@current_app.route('/')
def main():
  return render_template("base.html")

@current_app.route('/homepage') 
def home():
    """View for the Home page of your website."""
    agent = request.user_agent

    return render_template("home.html", agent=agent)

@current_app.errorhandler(404)
def page_not_found(error):
  return render_template('404.html'), 404

@current_app.route('/resume')
def resume():
  return render_template("resume.html")