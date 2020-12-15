from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from TitleFinder import TitleFinder
from AuthorFinder import AuthorFinder
from WebsiteObjectRetriever import WebsiteObjectRetriever
from WebsiteNameFinder import WebsiteNameFinder
from PublicationYearFinder import PublicationYearFinder
from CurrentDateFinder import CurrentDateFinder
import sqlite3

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # CB 2020-10-19 Get the url from the url box
        url = request.form.get("urlBox")

        # CB 2020-10-24 Initial variable values
        author = None
        title = None
        publicationYear = None
        response = None
        soup = None
        
        # CB 2020-10-19 try to make a GET request to the URL
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
        
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
        except Exception:
            return render_template("index.html", output=0, errorNumber=1)

        websiteObjectRetriever = WebsiteObjectRetriever(soup)
        deserializedJson = websiteObjectRetriever.retrieve()

        # Find Author
        try:
            authorFinder = AuthorFinder(soup, deserializedJson)
            author = authorFinder.find()

        except Exception:
            author = None

        # Find Title
        try:
            titleFinder = TitleFinder(soup)
            title = titleFinder.find()

        except Exception:
            title = None
        


        # Find Name of Website
        try:
            if author is None:
                websiteNameFinder = WebsiteNameFinder(soup, deserializedJson)
                author = websiteNameFinder.find()
        except Exception:
            author = None


        # Find Year Of Publication
        try:
            publicationYearFinder = PublicationYearFinder(soup)
            publicationYear = publicationYearFinder.find()
        except Exception:
            publicationYear = None
        
        # Get Current Date
        currentDateFinder = CurrentDateFinder()
        currentDate = currentDateFinder.find()

        return render_template("index.html", url=url, author=author, title=title, publicationYear=publicationYear, currentDate=currentDate)

    return render_template("index.html", output=0, errorNumber = 0)

@app.route("/unexpected-output")
def unexpected_output():
    return render_template("unexpected-output.html")

@app.route("/submit-unexpected-output")
def submit_unexpected_output():
    db = sqlite3.connect("HarvardReferenceGenerator.db")

    db.execute("INSERT INTO newUrls (url, expected_author, expected_title, \
        expected_website, expected_publication_year, user_email) \
            VALUES")