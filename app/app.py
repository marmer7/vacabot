import os
from datetime import datetime

import markdown
import openai
from dotenv import load_dotenv
from flask import (Flask, redirect, render_template, request,
                   send_from_directory)

from app.blog import extract_blog_dict, get_blog_posts
from app.itinerary import generate_itinerary, validate_destination

load_dotenv()  # take environment variables from .env.

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")


@app.before_request
def redirect_to_https():
    if request.headers.get("X-Forwarded-Proto") == "http":
        url = request.url.replace("http://", "https://", 1)
        return redirect(url, code=301)


@app.route("/")
def home():
    blog_posts = get_blog_posts()
    blog_posts = sorted(
        blog_posts, key=lambda blog_post: blog_post["date"], reverse=True
    )[:6]
    return render_template("home.html", blog_posts=blog_posts)


@app.route("/blog_posts")
def blog():
    blog_posts = get_blog_posts()
    blog_posts = sorted(
        blog_posts, key=lambda blog_post: blog_post["date"], reverse=True
    )
    return render_template("blog_posts.html", blog_posts=blog_posts)


@app.route("/blog_posts/<blog_id>")
def get_blog_post(blog_id: str):
    blog_post = extract_blog_dict(filename=f"{blog_id}.md")
    return render_template("blog_post.html", blog_post=blog_post)


@app.route("/search_flights")
def search_flights():
    return render_template("find_flight.html")


@app.route("/create_itinerary", methods=["GET", "POST"])
def create_itinerary():
    if request.method == "POST":
        destination = request.form["destination"]
        start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%d").date()
        end_date = datetime.strptime(request.form["end_date"], "%Y-%m-%d").date()
        interests = [
            interest.strip() for interest in request.form["interests"].split(",")
        ]

        cleaned_destination = validate_destination(destination)

        if cleaned_destination is None:
            itinerary = (
                f"{destination} is not a valid input. Please add a valid destination."
            )
        else:
            itinerary = generate_itinerary(
                cleaned_destination, start_date, end_date, interests
            )

        return render_template(
            "itinerary.html",
            title="Your Itinerary",
            destination=cleaned_destination,
            itinerary=markdown.markdown(itinerary),
        )
    else:
        return render_template("create_itinerary.html", title="Create Itinerary")


@app.route("/robots.txt")
def serve_robots():
    return send_from_directory(app.static_folder, "robots.txt")


@app.template_filter("markdown")
def convert_markdown_to_html(text):
    return markdown.markdown(text)


if __name__ == "__main__":
    app.run(debug=True)
