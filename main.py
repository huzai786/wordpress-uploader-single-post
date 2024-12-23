import sys
import os
import tomllib
# from credentials import username, password, site_url
from wordpressapi.media_crud import WordpressApiMediaCrud, MediaData
from wordpressapi.post_crud import WordpressApiPostCrud, PostData
from wordpressapi.category_crud import WordpressApiCategoryCrud, CategoryData
from wordpressapi.tag_crud import WordpressApiTagCrud, TagData

if not os.path.exists("credentials.toml"):
    sys.exit()

with open("credentials.toml", "r") as f:
    credentials = tomllib.loads(f.read()) 

username = credentials.get("username")
password = credentials.get("password")
site_url = credentials.get("site_url")

# get and verify credentials
if not username or not password or not site_url:
    print("Username or password or site url")
    sys.exit()

# get user input and verify it
with open("input.toml", "r") as f:
    toml_data_str = f.read()
toml_data_str = toml_data_str.replace("\\", "\\\\")

try:
    # Parse TOML data into a Python dictionary
    data = tomllib.loads(toml_data_str)

except tomllib.TOMLDecodeError as e:
    print("Error parsing TOML data:", e)

# ------------- input filtering -------------- # 
if not data["title"]:
    print("title missing")
    sys.exit()

title = data["title"]
featured_media_path = data["featured_media_path"]
categories = data["categories"]
content_path = data["content_path"]
content: str = data["content"]
tags = data["tags"]

content = content.strip("\n")
if not content_path and not content:
    print("Either enter content file path or add content")
    sys.exit()

if not content:
    with open(content_path, 'r', encoding='utf-8') as f:
        content = f.read()

if featured_media_path and not os.path.exists(featured_media_path):
    print(f"no image found at path {featured_media_path}!")
    sys.exit()

# ------------ categories ------------- #

category_ids = []
wpcategoryapi = WordpressApiCategoryCrud(username, password, site_url)
wordpress_categories: list[tuple[int, str]] = wpcategoryapi.get_categories() # list if id and name
for category in categories:  # categories is the input from user
    if category in [c[1] for c in wordpress_categories]: # meaning it is already created
        category_ids.append( [c[0] for c in wordpress_categories if c[1] == category][0] )
    else:
        # create that category
        cat_data = CategoryData(name=category)
        created, output = wpcategoryapi.create_category(cat_data)
        if created:
            category_ids.append(output.id)
        else:
            print("Failed to create category in wordpress due to unexpected error, try again later!")
            sys.exit()

# --------------- tags --------------- #
tag_ids = []
wptagapi = WordpressApiTagCrud(username, password, site_url)
wp_tags: list[tuple[int, str]] = wptagapi.get_tags()
for tag in tags:
    if tag in [t[1] for t in wp_tags]:
        tag_ids.append( [t[0] for t in wp_tags if t[1] == tag][0] )
    else:
        # create that tag
        tag_data = TagData(description=tag, name=tag)
        created, output = wptagapi.create_tag(tag_data)
        if created:
            tag_ids.append(output.id)

# ------------ featured media ------------ #

featured_media_id = None
if featured_media_path:
    wpmedia = WordpressApiMediaCrud(username, password, site_url)
    filename = os.path.basename(featured_media_path)
    media_input = MediaData(featured_media_path, filename, filename)
    created, output = wpmedia.create_media(media_input)
    if created:
        featured_media_id = output.id
    else:
        print("Failed to upload media to wordpress due to unexpected error, try again later!")
        sys.exit()

# ---------- creating post ----------- #

wppost = WordpressApiPostCrud(username, password, site_url)
if category_ids:
    post_data = PostData(title, content, category_ids, featured_media=featured_media_id, tags=tag_ids)
else:
    post_data = PostData(title=title, content=content, featured_media=featured_media_id, tags=tag_ids)


created, postid = wppost.create_post(post_data)
if created:
    print("post created id: ", postid.id)
else:
    print("unable to create post due to unexpected error please try again!")
    
