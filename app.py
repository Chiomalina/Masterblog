"""
A simple Flask blog application that allows users to create, update,
delete, and like posts stored in a JSON file.
"""

import json
import os
from datetime import datetime

from flask import (Flask, abort, redirect, render_template,
                   request, url_for)


app = Flask(__name__)

DATA_FILE = os.path.join(app.root_path, "posts.json")


def load_posts():
    """
    Load and return the list of posts from the JSON data file.

    Returns:
        list: A list of post dictionaries, or an empty list if the file
        does not exist.
    """
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_posts(posts):
    """
    Save the list of posts to the JSON data file, overwriting existing data.

    Args:
        posts (list): A list of post dictionaries to write.
    """
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(posts, file, indent=2, default=str)


def fetch_post_by_id(post_id):
    """
    Retrieve a single post by its ID.

    Args:
        post_id (int): The unique identifier of the post.

    Returns:
        dict or None: The matching post dictionary, or None if not found.
    """
    return next(
        (post for post in load_posts() if post.get("id") == post_id),
        None
    )


@app.route("/")
def home():
    """
    Redirect the root URL to the main index page.
    """
    return redirect(url_for("index"))


@app.route("/index")
def index():
    """
    Render the index page with all posts and the current timestamp.

    Returns:
        Response: Rendered template for the index page.
    """
    posts = load_posts()
    current_time = datetime.now()

    return render_template("index.html", posts=posts, date=current_time)


@app.route("/add", methods=["GET", "POST"])
def add():
    """
    Handle adding a new blog post via a form.

    GET:
        Render the blank form for creating a post.
    POST:
        Create a new post from form data, save it, and redirect to index.

    Returns:
        Response: Template render or redirect response.
    """
    if request.method == "POST":
        posts = load_posts()
        max_id = max(
            (post.get("id") for post in posts if isinstance(post.get("id"), int)),
            default=0
        )
        new_post = {
            "id": max_id + 1,
            "title": request.form.get("title"),
            "author": request.form.get("author"),
            "content": request.form.get("content"),
            "created": datetime.now()
        }
        posts.append(new_post)
        save_posts(posts)

        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/delete/<int:post_id>")
def delete(post_id):
    """
    Delete a post by its ID and update the JSON file.

    Args:
        post_id (int): The ID of the post to remove.

    Returns:
        Response: Redirect response to the index page.
    """
    posts = load_posts()
    posts = [post for post in posts if post.get("id") != post_id]
    save_posts(posts)

    return redirect(url_for("index"))


@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id):
    """
    Update an existing post's details via a form.

    GET:
        Render the form pre-populated with the post's data.
    POST:
        Apply changes from form data, save updates, and redirect to index.

    Args:
        post_id (int): The ID of the post to update.

    Returns:
        Response: Template render, redirect, or 404 if not found.
    """
    posts = load_posts()
    post = next((p for p in posts if p.get("id") == post_id), None)
    if post is None:
        abort(404)

    if request.method == "POST":
        post["title"] = request.form.get("title", post["title"])
        post["author"] = request.form.get("author", post["author"])
        post["content"] = request.form.get("content", post["content"])
        save_posts(posts)

        return redirect(url_for("index"))

    return render_template("update.html", post=post)


@app.route("/like/<int:post_id>", methods=["GET", "POST"])
def like(post_id):
    """
    Increment the like-counter for a post and show confirmation.

    Args:
        post_id (int): The ID of the post being liked.

    Returns:
        Response: Rendered 'like.html' template or 404 if not found.
    """
    posts = load_posts()
    post = next((p for p in posts if p.get("id") == post_id), None)
    if post is None:
        abort(404)

    post["likes"] = post.get("likes", 0) + 1
    save_posts(posts)

    return render_template("like.html", post=post)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
