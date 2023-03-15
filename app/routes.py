import os

import markdown
import requests
from flask import (jsonify, redirect, render_template, request,
                   send_from_directory, url_for)

from app import app, db
from app.blog import extract_blog_dict, get_blog_posts
from app.itinerary import ItineraryForm, generate_itinerary
from app.models import Itinerary


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
    form = ItineraryForm()

    if form.validate_on_submit():
        destination = form.destination.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        interests = [interest.strip() for interest in form.interests.data.split(",")]

        itinerary_markdown = generate_itinerary(
            destination, start_date, end_date, interests
        )
        itinerary = Itinerary(
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            interests=interests,
            markdown=itinerary_markdown,
        )
        db.session.add(itinerary)
        db.session.commit()
        return redirect(url_for("get_itinerary", id=itinerary.id), code=301)

    return render_template("create_itinerary.html", title="Create Itinerary", form=form)


@app.route("/itinerary/<int:id>")
def get_itinerary(id):
    itinerary = Itinerary.query.get(id)
    if itinerary:
        return render_template(
            "itinerary.html",
            id=id,
            title="Your Itinerary",
            destination=itinerary.destination,
            itinerary=markdown.markdown(itinerary.markdown),
        )
    else:
        return redirect(url_for("create_itinerary"), code=301)


@app.route("/robots.txt")
def serve_robots():
    return send_from_directory(app.static_folder, "robots.txt")


@app.route("/disclaimer")
def disclaimer():
    return render_template("disclaimer.html")


@app.route("/api/autocomplete", methods=["GET"])
def autocomplete():
    query = request.args.get("input", "")
    if not query:
        return jsonify({"error": "Missing input parameter."}), 400

    url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={query}&types=(cities)&key={os.getenv('GOOGLE_PLACES_API_KEY')}"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data from Google Places API."}), 500

    data = response.json()
    return jsonify(data)


@app.errorhandler(404)
def catch_all(e):
    return render_template("404.html"), 404


@app.template_filter("markdown")
def convert_markdown_to_html(text):
    return markdown.markdown(text)
