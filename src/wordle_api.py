# ------------------------------------------------------------------------------
# wordle_api.py
#
# March 2022, Connor Ayre, Tom Zhu, Zakaria Ismail
#
# Copyright (c) 2022
# All rights reserved.
# ------------------------------------------------------------------------------

class WordleAPI:
    """
    Wordle API object.
    """
    def __init__(self, url):
        self.url = url
        self.id = None
        self.key = None
    
    def _startGame(self):
        """
        Start game via the API
        """
        # Send POST request to url that starts game
        return True
    
    def sendGuess(self, guess):
        """
        Send a guess to the API
        """
        pass


class ResponseEvent:
    """
    Response event object describing result of API guess request
    """
    def __init__(self, status, data):
        self.status = status
        self.data = data
