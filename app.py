from flask import Flask, render_template, request, session
import os
import requests
import sqlite3
from bs4 import BeautifulSoup
from TitleFinder import TitleFinder
from AuthorFinder import AuthorFinder
from WebsiteObjectRetriever import WebsiteObjectRetriever
from WebsiteNameFinder import WebsiteNameFinder
from PublicationYearFinder import PublicationYearFinder
from CurrentDateFinder import CurrentDateFinder

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/", methods=["GET", "POST"])
def index():
    '''
        The method that is called when the website is first run and when the user 
        enters a URL.
        GET return: just the webpage
        POST return: the webpage with the author, title, 
        publicationYear, url and currentDate variables to be put into the Harvard
        Reference.
    '''
    if request.method == "POST":
        # CB 2020-10-19 Get the url from the url box
        url = request.form.get("urlBox")
        session["url"] = url

        # CB 2020-10-24 Initial variable values
        author = None
        title = None
        publicationYear = None
        response = None
        soup = None
        
        # CB 2020-10-19 try to make a GET request to the URL
        headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0"}
        
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
    '''
        The method that is called when the user selects the link on the index page
        that indicates that it was not the output they were expecting.
    '''
    return render_template("unexpected-output.html")

@app.route("/submit-unexpected-output", methods=["POST"])
def submit_unexpected_output():
    '''
        The method that is called when the user submits details on what they were 
        expecting the outcome to be of the Harvard Reference.
        Returns: The index page with the variables that they inputted into the form to make 
        a Harvard Reference.
    '''

    db = sqlite3.connect("HarvardReferenceGenerator.db")
    url = session["url"]
    expected_author = request.form.get("author")
    expected_title = request.form.get("title")
    expected_website_name = request.form.get("websiteName")
    expected_publication_year = request.form.get("publicationYear")
    user_email = request.form.get("userEmail")
    currentDateFinder = CurrentDateFinder()
    currentDate = currentDateFinder.find()

    urlOccurence = db.execute("SELECT * FROM newUrls WHERE url=?", (url,)).fetchall()

    if len(urlOccurence) < 1:
        db.execute("INSERT INTO newUrls (url, expected_author, expected_title, expected_website_name, expected_publication_year, user_email) VALUES (?, ?, ?, ?, ?, ?)", (url, expected_author, expected_title, expected_website_name, expected_publication_year, user_email))
        db.commit()

    return render_template("index.html", url=url, author=expected_author, title=expected_title, publicationYear=expected_publication_year, currentDate=currentDate)
