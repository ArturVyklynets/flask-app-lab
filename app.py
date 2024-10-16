from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def main():
  return 'Hello, world!', 200

@app.route('/homepage') 
def home():
    """View for the Home page of your website."""
    agent = request.user_agent

    return f"This is your homepage :)  - {agent}"

@app.route("/hi/<string:name>")
def greetings(name):
   name = name.upper()
   age = request.args.get("age", 0, int)
   year = 2024 - age
   return f"Welcome, {name} - {year}"

if __name__ == "__main__":
    app.run()  # Launch built-in web server and run this Flask webapp, debug=True