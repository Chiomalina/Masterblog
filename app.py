import json
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import uuid

app = Flask(__name__)

blog_posts = []


@app.route("/")
def hello_world():
	return "Hello, World!"

@app.route("/index")
def index():
	# 1. Open and load the JSON file
	with open("posts.json", "r", encoding="utf-8") as fileobject:
		loaded_post = json.load(fileobject)

	# 2. Pass the list of posts into the template
	return render_template("index.html", posts=loaded_post)




@app.route("/add", methods=["GET", "POST"])
def add():
	if request.method == "POST":
		# 1. pull values out of the form
		title = request.form.get("title", None)
		author = request.form.get("author", None)
		content = request.form.get("content", None)

		# 2. Assemble a new post object (additional functionality: timestamp added.)
		new_post = {
			"id": str(uuid.uuid4()),
			"title": title,
			"author": author,
			"content": content,
			"created": datetime.utcnow()
		}

		# 3. Save it by appending it to empty blog_post above
		blog_posts.append(new_post)

		# 4. Go back to home so users can see the updated list
		return redirect(url_for("index"))

	# Display the blank form if it's a GET request
	return(render_template("add.html"))





if __name__=="__main__":
	app.run(host="0.0.0.0", port=5001, debug=True)