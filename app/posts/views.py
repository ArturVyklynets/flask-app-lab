import json, os
from . import post_bp
from datetime import datetime
from flask import render_template, request, abort, flash, redirect, url_for, session
from .forms import PostForm
from .models import Post
from .utils import *
from app import db

@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        post_new = Post(title=title, content=content)
        db.session.add(post_new)
        db.session.commit()
        flash(f'Post {title} added successfully!', 'success')
        return redirect(url_for('.add_post'))
    elif form.errors:
        flash(f"Enter the correct data in the form!", "danger")
   
    return render_template("add_post.html", form=form)


# @post_bp.route('/add_post', methods=['GET', 'POST'])
# def add_post():
#   form = PostForm()
#   if form.validate_on_submit():
#       title = form.title.data
#       content = form.content.data
#       # category = form.category.data
#       # is_active = form.is_active.data
#       publish_date =  form.publish_date.data.strftime('%Y-%m-%d')
#       # author = session.get('username', 'Anonymous')
#       # current_posts = load_posts()
#       # new_post = {
#       #       "title": title,
#       #       "content": content,
#       #       "publication_date": publish_date,
#       # }
#           #  "category": category,
#             # "author": author
#       #  
#       new_post = Post(title,content, publish_date)
#       db.session.add(new_post)
#       db.session.commit()

#       flash(f'Пост "{title}" успішно додано!', 'success')
#       return redirect(url_for('.get_posts'))
#   elif request.method == "POST":
#       flash(f'Enter the correct data in form', 'danger')
#   return render_template('add_post.html', form=form)

@post_bp.route('/') 
def get_posts():
    stmt = db.select(Post).order_by(Post.title)
    all_posts = db.session.scalars(stmt).all()
    return render_template("posts.html", posts=all_posts)

@post_bp.route('/<int:id>') 
def detail_post(id):
    stmt = db.select(Post).filter_by(id=id)
    post = db.session.scalar(stmt)
    if post is None:
        abort(404)
    return render_template("detail_post.html", post=post)
