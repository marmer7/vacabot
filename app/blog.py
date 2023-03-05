import os
import re

import markdown


def extract_blog_dict(filename: str):
    blog_metadata = {"id": filename[:-3]}

    with open(os.path.join("../blog", filename), "r") as f:
        content = f.read()
        keys = ["title", "date"]
        # extract title from first line of markdown file

        for key in keys:
            pattern = f"^{key}=(.*)$"
            value = (
                re.search(pattern, content, re.MULTILINE | re.IGNORECASE)
                .group(1)
                .strip()
            )

            blog_metadata[key] = value

            pattern = f"^{key}=.*\n"
            content = re.sub(pattern, "", content, flags=re.MULTILINE | re.IGNORECASE)

        # Convert markdown to HTML
        html = markdown.markdown(content)
        blog_metadata["html"] = html

    return blog_metadata


def get_blog_posts():
    blog_posts = []
    for filename in os.listdir("../blog"):
        if filename.endswith(".md"):
            blog_post = extract_blog_dict(filename=filename)
            blog_posts.append(blog_post)
    return blog_posts
