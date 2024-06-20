import json
import requests
from typing import NamedTuple

class TagOutput(NamedTuple):
    id: int | None 
    slug: str
    tag_link: str

class TagData(NamedTuple):
    description: str | None = None
    name: str | None = None
    slug: str | None = None


class WordpressApiTagCrud:
    url_tags = '/wp-json/wp/v2/tags'
    headers = {"Content-Type": "application/json; charset=utf-8"}

    def __init__(self, username, password, siteurl) -> None:
        self.username = username
        self.password = password
        self.siteurl = siteurl

    def create_tag(self, data: TagData) -> tuple[bool, TagOutput | None]:
        try:     
            response = requests.post(self.siteurl + self.url_tags, data=json.dumps(data._asdict()), 
                                     headers=self.headers, auth=(self.username, self.password))
            if response.status_code in(200, 201):
                id=response.json()["id"]
                slug=response.json()["slug"]
                link=response.json()["link"]
                tag_output = TagOutput(id=id, slug=slug, tag_link=link)

                return True, tag_output
            else:
                return False, response.json()
            
        except requests.RequestException as e:
            print(e)
            return False, None
        
    def get_tags(self) -> list[tuple[int, str]]:
        """get a list of tags id and their name"""
        try:
            res = requests.get(self.siteurl + self.url_tags, auth=(self.username, self.password), 
                               headers=self.headers)
        
            if res.status_code == 200:
                tagdata = []
                for data in res.json():
                    tagdata.append((data['id'], data['name']))
                return tagdata
            else:
                return []
            
        except requests.RequestException as e:
            print(e)
            return []
        