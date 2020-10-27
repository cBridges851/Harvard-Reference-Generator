class OrdinalRetriever():
    def __init__(self, day):
        self.day = day

    def retrieveOrdinal(self):
        suffixes = {
            1: "st",
            2: "nd",
            3: "rd"
        }

        if self.day == 24:
            return "th"

        return suffixes.get(self.day % 10, "th")