class WebsiteNameFinder():
    def __init__(self, soup, deserializedJson):
        self.soup = soup
        self.deserializedJson = deserializedJson

    def find(self):
        if self.deserializedJson is not None:
            return self.deserializedJson["publisher"]["name"]
        
        websiteNameMeta = self.soup.find(attrs={"property" : "og:site_name"})
        return websiteNameMeta.attrs["content"]