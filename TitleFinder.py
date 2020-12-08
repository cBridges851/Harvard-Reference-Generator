class TitleFinder():
    def __init__(self, soup):
        self.soup = soup

    def find(self):
        if self.soup.find("h1") is not None:
            return self.soup.find("h1").get_text()
            
        if self.soup.find("title") is not None:
            return self.soup.find("title").get_text()
            
        