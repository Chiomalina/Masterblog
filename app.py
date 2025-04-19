import json
import os
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime


app = Flask(__name__)


DATA_FILE = os.path.join(app.root_path, "posts.json")

def load_posts():
	"""Return a list of posts (empty if file doesn't exist)."""
	if not os.path.exists(DATA_FILE):
		return []
	with open(DATA_FILE, "r", encoding="utf-8") as fileobject:
		return json.load(fileobject)


def save_posts(posts):
	"""Overwrite posts.json with the given list."""
	with open(DATA_FILE, "w", encoding="utf-8") as fileobject:
		# default=str is used to ensure datetime is JSON-serializable if we choose to keep the UTC timestamps
		json.dump(posts, fileobject, indent=2, default=str)


def fetch_post_by_id(post_id):
	"""
	Load all posts and return the one whose integer 'id' matches post_id.
	Returns None if no such post exists.
	"""
	posts = load_posts()
	return next((p for p in posts if p.get('id') == post_id), None)


@app.route("/")
def home():
	return redirect(url_for("index"))


@app.route("/index")
def index():
	# 1. Retrieve data from load_posts()
	posts = load_posts()
	created = datetime.now()

	# 2. Pass the list of posts into the template
	return render_template("index.html", posts=posts, date=created)


@app.route("/add", methods=["GET", "POST"])
def add():
	if request.method == "POST":
		# 1. Load up the existing posts
		posts = load_posts()
		print("Loaded posts:", posts)

		# 2. Compute the next integer ID
		#    We guard with default=0 so max([]) -> 0
		max_id = max(
			(post.get("id") for post in posts if isinstance(post.get("id"), int)),
			default=0
		)
		next_id = max_id + 1

		# 3. pull values out of the form
		title = request.form.get("title", None)
		author = request.form.get("author", None)
		content = request.form.get("content", None)
		created = request.form.get("created", None)

		# 4. Assemble a new post object, now with an integer ID (additional functionality: timestamp added.)
		new_post = {
			"id": next_id,
			"title": title,
			"author": author,
			"content": content,
			"created": datetime.now()
		}

		# 5. Save it by appending it to empty blog_post above
		posts.append(new_post)
		save_posts(posts)

		# 4. Go back to home so users can see the updated list
		return redirect(url_for("index"))

	# Display the blank form if it's a GET request
	return(render_template("add.html"))


@app.route("/delete/<int:post_id>")
def delete(post_id):
	# 1. Load existing posts
	posts = load_posts()

	# 2. Filter out the post with the matching id.
	# This is another logic for deleting the post with post_id instead of using the delete method
	posts = [post for post in posts if post.get("id") != post_id]

	# 3. Save the updated list back to JSON
	save_posts(posts)

	# 4. Redirect back to the index page
	return redirect(url_for("index"))


@app.route("/update/<int:post_id>", methods=["GET", "POST"])
def update(post_id):
	# 1. Load the full list of posts
	posts = load_posts()

	# 2. Find the post in that list
	post = next((p for p in posts if p.get("id") == post_id), None)
	if post is None:
		return "Post not found", 404

	if request.method == 'POST':
		# 3. Update its fields
		# Update fields from the form (fall back to existing values)
		post['title'] = request.form.get('title', post['title'])
		post['author'] = request.form.get('author', post['author'])
		post['content'] = request.form.get('content', post['content'])

		# 4. Save the update list back to disk
		save_posts(posts)

		return redirect(url_for('index'))

	# GET: render the pre-populated form
	return render_template('update.html', post=post)

@app.route('/like/<int:post_id>')
def like(post_id):
	posts = load_posts()
	for post in posts:
		if post.get('id') == post_id:
			post['likes'] = post.get('likes', 0) + 1
			break
	save_posts(posts)
	return redirect(url_for('index'))



if __name__=="__main__":
	app.run(host="0.0.0.0", port=5001, debug=True)