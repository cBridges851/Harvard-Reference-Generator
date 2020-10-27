from datetime import date
from OrdinalRetriever import OrdinalRetriever

class CurrentDateFinder():
    def __init__(self):
        pass

    def find(self):
        currentDate = date.today()
        day = currentDate.day
        ordinal = OrdinalRetriever(day).retrieveOrdinal()

        returnString = f"{day}{ordinal} {currentDate.strftime('%b')} {currentDate.year}"
        return returnString
