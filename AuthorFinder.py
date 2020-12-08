import re

class AuthorFinder():
    def __init__(self, soup, deserializedJson):
        self.soup = soup
        self.deserializedJson = deserializedJson

    def find(self):
        if self.soup.findAll("link") is not None:
            allLinkTags = self.soup.findAll("link")
            for linkTag in allLinkTags:
                if linkTag.get("content") is not None:
                    return linkTag.get("content")

        if self.deserializedJson is not None:
            try:
                author = self.deserializedJson["author"]["name"]
                author = author.split(" ")

                # Based on BBC Webpage
                if len(author) == 3:
                    return author[2] + ", " + author[1][0] + "."

                if len(author) == 2:
                    return author[1] + ", " + author[0][0] + "."

            except Exception:
                return self.deserializedJson["page"]["pageInfo"]["publisher"]
            except Exception as e:
                print(f"Unable to retrieve info: {e}")

        # Based on Psychology Today
        if self.soup.find(class_="blog-entry__date--full fine-print") is not None:
            author = self.soup.find(class_="blog-entry__date--full fine-print").get_text()
            author = re.findall(r"(?<=By ).*(?= published)", author)[0]
            author = author.split(" ")
            return author[1] + ", " + author[0][0] + "."