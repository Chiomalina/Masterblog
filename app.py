import json
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
	return "Hello, World!"

@app.route("/index")
def index():
	# 1. Open and load the JSON file
	with open("posts.json", "r", encoding="utf-8") as fileobject:
		blog_posts = json.load(fileobject)

	# 2. Pass the list of posts into the template
	return render_template("index.html", posts=blog_posts)


if __name__=="__main__":
	app.run(host="0.0.0.0", port=5001, debug=True)