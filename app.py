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

@app.route("/hi/<string:name>/<int:age>")
def greetings(name, age):
   name = name.upper()
   return f"Welcome, {name} - {age}"

if __name__ == "__main__":
    app.run()  # Launch built-in web server and run this Flask webapp, debug=True