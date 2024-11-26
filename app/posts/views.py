import json, os
from . import post_bp
from datetime import datetime
from flask import render_template, request, abort, flash, redirect, url_for, session
from .forms import PostForm
from .models import Post
from app import db

@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        is_active = form.is_active.data
        category = form.category.data
        publish_date =  form.publish_date.data
        author = session.get('username', 'Anonymous')
        post_new = Post(title=title, content=content, is_active=is_active, category=category, author=author, posted=publish_date)
        db.session.add(post_new)
        db.session.commit()
        flash(f'Post {title} added successfully!', 'success')
        return redirect(url_for('.add_post'))
    elif form.errors:
        flash(f"Enter the correct data in the form!", "danger")
   
    return render_template("add_post.html", form=form, edit=False)

@post_bp.route('/') 
def get_posts():
    stmt = db.select(Post).order_by(Post.posted)
    all_posts = db.session.scalars(stmt).all()
    return render_template("posts.html", posts=all_posts)

@post_bp.route('/<int:id>') 
def detail_post(id):
    post = db.get_or_404(Post, id)
    return render_template("detail_post.html", post=post)

@post_bp.route('/delete_post/<int:id>') 
def delete_post(id):
    post = db.get_or_404(Post, id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('.get_posts'))

@post_bp.route('/edit_post/<int:id>', methods=['GET', 'POST']) 
def edit_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)
    form.publish_date.data = post.posted
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.is_active = form.is_active.data
        post.category = form.category.data
        post.posted = form.publish_date.data
        db.session.commit()
        flash(f'Post updated successfully!', 'success')
        return redirect(url_for('.get_posts'))
    elif form.errors:
        flash(f"Enter the correct data in the form!", "danger")
    return render_template("add_post.html", form=form, edit=True)