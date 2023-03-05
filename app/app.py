import os

import markdown
import openai
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request

from app.blog import extract_blog_dict, get_blog_posts

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
def flights():
    return render_template("find_flight.html")


@app.route("/create_itinerary", methods=["GET", "POST"])
def create_itinerary():
    if request.method == "POST":
        destination = request.form["destination"]
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        interests = request.form["interests"].split(",")

        with open("app/prompts/itinerary.txt", "r", encoding="utf-8") as f:
            prompt = f.read()

        user_input = "\n".join(
            [
                "Input:",
                "CurrentDate=2023-03-01",
                f"Destination={destination}",
                f"StartDate={start_date}",
                f"EndDate={end_date}",
                f"Interests={str(interests)}",
                "Output:",
            ]
        )

        prompt = f"{prompt}\n{user_input}"
        print(prompt)
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=2400,
            n=1,
            stop=None,
            temperature=0.7,
        )
        itinerary = response.choices[0].text.strip()
        return render_template(
            "itinerary.html", title="Your Itinerary", itinerary=itinerary
        )
    else:
        return render_template("create_itinerary.html", title="Create Itinerary")


@app.template_filter("markdown")
def convert_markdown_to_html(text):
    return markdown.markdown(text)


if __name__ == "__main__":
    app.run(debug=True)
