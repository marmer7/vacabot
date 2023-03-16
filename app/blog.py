import os
import re

import markdown


def extract_blog_dict(filename: str):
    blog_metadata = {"id": filename[:-3]}

    with open(os.path.join("./blog_posts", filename), "r") as f:
        content = f.read()
        keys = ["title", "date", "description", "keywords", "modified"]
        # extract title from first line of markdown file

        for key in keys:
            pattern = f"^{key}=(.*)$"

            search = re.search(pattern, content, re.MULTILINE | re.IGNORECASE)
            if search is not None:
                value = search.group(1).strip()
                pattern = f"^{key}=.*\n"
                content = re.sub(
                    pattern, "", content, flags=re.MULTILINE | re.IGNORECASE
                )
            else:
                value = ""

            blog_metadata[key] = value

        if blog_metadata.get("date"):
            sort_date = (
                blog_metadata["modified"]
                if blog_metadata.get("modified")
                else blog_metadata["date"]
            )
            blog_metadata["sort_date"] = sort_date
        else:
            blog_metadata["sort_date"] = "1999-01-01"

        # Convert markdown to HTML
        html = markdown.markdown(content)
        blog_metadata["html"] = html

    return blog_metadata


def get_blog_posts():
    blog_posts = []
    for filename in os.listdir("./blog_posts"):
        if filename.endswith(".md"):
            blog_post = extract_blog_dict(filename=filename)
            blog_posts.append(blog_post)
    return blog_posts
