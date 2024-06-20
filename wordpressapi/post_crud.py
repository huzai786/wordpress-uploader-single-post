import json
from typing import NamedTuple
import requests


class PostOutput(NamedTuple):
    id: str | None
    slug: str

class PostData(NamedTuple):
    title: str | None = None
    content: str | None = None
    categories: list[int] | None = None
    tags: list[int] | None = None
    featured_media: int | None = None
    status: str = "publish"
    comment_status: str = "open"
    ping_status: str = "open"
    sticky: bool = False
    

class WordpressApiPostCrud:
    url_posts = '/wp-json/wp/v2/posts'
    headers = {"Content-Type": "application/json; charset=utf-8"}
    
    def __init__(self, username, password, site_url) -> None:
        self.username = username
        self.password = password
        self.siteurl = site_url

    def create_post(self, data: PostData) -> tuple[bool, PostOutput | None]:
        try:    
            response = requests.post(self.siteurl + self.url_posts, data=json.dumps(data._asdict()), 
                                     headers=self.headers, auth=(self.username, self.password))
            if response.status_code in(200, 201):
                return True, PostOutput(id=response.json()["id"], slug=response.json()["slug"]) 
            else:
                return False, None
        except requests.RequestException as e:
            print(e)
            return False, None
    