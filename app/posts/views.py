import json, os
from . import post_bp
from datetime import datetime
from flask import render_template, abort, flash, redirect, url_for, session
from .forms import PostForm
posts = [
    {"id": 1, 'title': 'My First Post', 'content': 'This is the content of my first post.', 'author': 'John Doe'},
    {"id": 2, 'title': 'Another Day', 'content': 'Today I learned about Flask macros.', 'author': 'Jane Smith'},
    {"id": 3, 'title': 'Flask and Jinja2', 'content': 'Jinja2 is powerful for templating.', 'author': 'Mike Lee'}
] 

POSTS_FILE = './app/static/posts/posts.json'

def load_posts():
    if not os.path.exists(POSTS_FILE):
        return []
    
    with open(POSTS_FILE, 'r') as f:
      try:
          return json.load(f)
      except json.decoder.JSONDecodeError:
          print("Error: The JSON file is malformed.")
          return []

def save_posts(posts):
  for post in posts:
    if isinstance(post.get('publication_date'), datetime):
        post['publication_date'] = post['publication_date'].strftime('%Y-%m-%d')
  with open(POSTS_FILE, 'w') as f:
      json.dump(posts, f, indent=4)


@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
  form = PostForm()
  if form.validate_on_submit():
      title = form.title.data
      content = form.content.data
      category = form.category.data
      is_active = form.is_active.data
      publish_date =  form.publish_date.data.strftime('%Y-%m-%d')
      author = session.get('username', 'Anonymous')
      current_posts = load_posts()
      new_id = current_posts[-1]['id'] + 1 if current_posts else 1
      new_post = {
            "id": new_id,
            "title": title,
            "content": content,
            "category": category,
            "is_active": is_active,
            "publication_date": publish_date,
            "author": author
      }

      current_posts.append(new_post)
      save_posts(current_posts)

      flash(f'Пост "{title}" успішно додано!', 'success')
      return redirect(url_for('.get_posts'))

  return render_template('add_post.html', form=form)

@post_bp.route('/') 
def get_posts():
    all_posts = load_posts()
    return render_template("posts.html", posts=all_posts)

@post_bp.route('/<int:id>') 
def detail_post(id):
    all_posts = load_posts()
    post = next((post for post in all_posts if post["id"] == id), None)
    if post is None:
        abort(404)
    return render_template("detail_post.html", post=post)
