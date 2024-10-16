from flask import Flask
app = Flask(__name__)

@app.route('/')
def main():
  return 'Hello, world!', 200

@app.route('/homepage') 
def home():
    """View for the Home page of your website."""

    return "This is your homepage :) "

if __name__ == "__main__":
    app.run()  # Launch built-in web server and run this Flask webapp, debug=True