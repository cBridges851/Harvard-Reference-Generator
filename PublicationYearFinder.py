import re
from datetime import date

class PublicationYearFinder():
    def __init__(self, soup):
        self.soup = soup

    def find(self):
        # Website uses a time tag
        if self.soup.find("time") is not None:
            try:
                return self.soup.find("time").attrs["datetime"][0:4]
            except Exception:
                timeTag = self.soup.find("time").get_text()
                return re.findall(r"[0-9]{4}", timeTag)[0]

        try:
            publishedYearMeta = self.soup.find(attrs={"itemprop" : "datePublished"})
            return publishedYearMeta.attrs["content"][0:4]
        
        # Based on Psychology Today
        except Exception:
            fullDate = self.soup.find(class_="magazine-cover-feature-date__date").get_text()
            return re.findall(r"[0-9]{4}", fullDate)[0]
        
        return date.today().year