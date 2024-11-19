import json, os
from . import post_bp
from datetime import datetime
from flask import render_template, request, abort, flash, redirect, url_for, session
from .forms import PostForm
from .models import Post
from .utils import *

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

      save_post(new_post)

      flash(f'Пост "{title}" успішно додано!', 'success')
      return redirect(url_for('.get_posts'))
  elif request.method == "POST":
      flash(f'Enter the correct data in form', 'danger')
  return render_template('add_post.html', form=form)

@post_bp.route('/') 
def get_posts():
    all_posts = load_posts()
    return render_template("posts.html", posts=all_posts)

@post_bp.route('/<int:id>') 
def detail_post(id):
    post = get_post(id)
    if post is None:
        abort(404)
    return render_template("detail_post.html", post=post)
