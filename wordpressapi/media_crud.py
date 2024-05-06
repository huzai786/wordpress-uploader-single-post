from typing import NamedTuple
import requests


class MediaData(NamedTuple):
    file_path: str | bytes
    file_name: str
    alt_text: str | None = ''
    caption: str | None = ''
    

class MediaOutput(NamedTuple):
    id: str | None
    slug: str = ''
    link: str = ''
    alt_text: str = ''
    title: str = ''

class WordpressApiMediaCrud:
    url_media = '/wp-json/wp/v2/media'
    headers = {"Content-Type": "application/json; charset=utf-8"}

    def __init__(self, username, password, siteurl) -> None:
        self.username = username
        self.password = password
        self.siteurl = siteurl

    def create_media(self, media_data: MediaData) -> tuple[bool, MediaOutput | None]:
        image_name = media_data.file_name
        if isinstance(media_data.file_path, str):
            img_data = open(media_data.file_path, 'rb').read()
        else:
            img_data = media_data.file_path
            
        img_header = { 
            'Content-Type': 'image/png',
            'Content-Disposition' : 'attachment; filename=%s'% image_name
        }
        
        res = requests.post(self.siteurl + self.url_media, data=img_data,
                            auth=(self.username, self.password), headers=img_header)
        if res.status_code == 201:
            output = MediaOutput(id=res.json()["id"], 
                                 slug=res.json()["slug"],
                                 link=res.json()['guid']['rendered'],
                                 alt_text=media_data.alt_text, # type: ignore
                                 title=res.json()["title"]["rendered"]
                                )
            return True, output
        else:
            print(res.json())
            return False, None
