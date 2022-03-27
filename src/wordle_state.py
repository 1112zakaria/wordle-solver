# ------------------------------------------------------------------------------
# wordle_state.py
#
# March 2022, Connor Ayre, Tom Zhu, Zakaria Ismail
#
# Copyright (c) 2022
# All rights reserved.
# ------------------------------------------------------------------------------

# Imports
from wordle_ai import WordleAI
from wordle_api import WordleAPI
from string import ascii_lowercase

class WordleState:
    """
    WordleState object storing current game state, including
    guess history, letter status. 
    """
    def __init__(self):
        self.ai = WordleAI()
        self.api = WordleAPI()
        self.outputs = []       # objects that can print/output game state
        self.word_history = []
        self.letter_status = {}
        
        for letter in ascii_lowercase:
            # Initialize letter -> status MAP
            self.letter_status[letter] = 0    

    def runGame(self):
        pass

