import json


class WebsiteObjectRetriever():
    def __init__(self, soup):
        self.soup = soup

    def retrieve(self):
        try:
            scriptTag = self.soup.find("script")
            scriptTagContents = scriptTag.contents
            return json.loads(scriptTagContents[0])
        except Exception:
            return None