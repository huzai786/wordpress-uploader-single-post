import json
import requests
from typing import NamedTuple


class CategoryData(NamedTuple):
    description: str | None = None
    name: str | None = None
    slug: str | None = None
    parent: int | None = None

class CategoryOutput(NamedTuple):
    count: int
    link: str
    slug: str
    id: int | None = None


class WordpressApiCategoryCrud:
    wp_category_url = "/wp-json/wp/v2/categories"
    headers = {"Content-Type": "application/json; charset=utf-8"}
    
    def __init__(self, username, password, site_url) -> None:
        self.username = username
        self.password = password
        self.siteurl = site_url
        
    def create_category(self, data: CategoryData) -> tuple[bool, CategoryOutput | None]:
        try:
            response = requests.post(self.siteurl + self.wp_category_url, data=json.dumps(data._asdict()), headers=self.headers, auth=(self.username,self.password))
            if response.status_code in (200, 201):
                cat_id = response.json()['id']
                cnt = response.json()['count']
                link = response.json()['link']
                slug = response.json()['slug']
                catout = CategoryOutput(id=cat_id, count=cnt, link=link, slug=slug)
                return True, catout
            else:
                print("error encountered!", response.json())
                return False, response.json()
            
        except requests.RequestException as e:
            print(e)
            return False, None
        
    def get_categories(self) -> list[tuple[int, str]]:
        """get a list of categories id and their name"""
        try:
            res = requests.get(self.siteurl + self.wp_category_url, auth=(self.username, self.password), 
                               headers=self.headers)
        
            if res.status_code == 200:
                catdata = []
                for data in res.json():
                    catdata.append((data['id'], data['name']))
                return catdata
            else:
                return []
            
        except requests.RequestException as e:
            print(e)
            return []
        