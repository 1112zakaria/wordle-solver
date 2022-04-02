# ------------------------------------------------------------------------------
# wordle_ai.py
#
# March 2022, Connor Ayre, Tom Zhu, Zakaria Ismail
#
# Copyright (c) 2022
# All rights reserved.
# ------------------------------------------------------------------------------

"""
Possible optimizations:
- save keep_map and remove_map as attributes and
    append new discovered values instead of repetitively
    (up to 6 times) computing this info
"""

# Python imports
from enum import Enum
from typing import List
import math

class LetterState(Enum):
    GREY    = 0
    YELLOW  = 1
    GREEN   = 2

class WordleAI:

    def __init__(self, words: set):
        self.possible_words = words

    def prune_words(self, game_state):
        """
        Prune words from the set of words.

        Args:
            - game_state ('List[Dict]): list of dictionaries describing guess outcomes
        """
        keep_map = self._get_keep_map(game_state)
        remove_map = self._get_remove_map(game_state)
        for word in self.possible_words:
            to_remove = False
            for position in range(len(word)):
                letter = word[position]

                # Remove words where letter->position combo are in remove_map
                if letter in remove_map and position in remove_map[letter]:
                    to_remove = True

                # Remove words where position->letter are not in keep_map
                if keep_map[position] != [] and letter not in keep_map[position]:
                    to_remove = True

            if to_remove:
                self.possible_words.remove(word)
        

    def _get_keep_map(self, game_state: dict) -> dict:
        """
        Gets position->letters list MAP describing criteria 
        of words to not prune

        Args:
            - game_state ('List[dict]): list of dictionaries describing guess outcomes
        Returns:
            - ('dict'): critieria of words to not prune
        """
        keep_map = {
            0: [],
            1: [],
            2: [],
            3: [],
            4: []
        }
        for guess in game_state:
            letter = guess['letter']
            state = guess['state']
            position = guess['position']

            if state == LetterState.GREEN:
                # add letter to position's list
                # Q: should I also add to all other positions?
                if letter not in keep_map[position]: keep_map[position].append(letter)
            
            if state == LetterState.YELLOW:
                # add letter to all other positions' lists
                for i in range(0, 5):
                    if i != position:
                        if letter not in keep_map[position]: keep_map[i].append(letter)
            
        return keep_map
    
    def _get_remove_map(self, game_state) -> dict:
        """
        Gets letter->positions list MAP describing criteria of
        words to prune

        Args:
            - game_state ('List[dict]): list of dictionaries describing guess outcomes
        Returns:
            - ('dict'): criteria of words to prune
        """
        remove_map = {}
        for guess in game_state:
            letter = guess['letter']
            state = guess['state']
            position = guess['position']

            if state == LetterState.YELLOW:
                # Remove letter for single position
                if letter not in remove_map:
                    remove_map[letter] = []
                remove_map[letter].append(position)

            if state == LetterState.GREY:
                # Remove letter for all positions
                if letter not in remove_map:
                    remove_map[letter] = []
                remove_map[letter] += [0,1,2,3,4]
        
        return remove_map

    #***********************************************************************************************************
    #function to calculate entropy (expected value of information), returns a float
    #Args:
    #     - word: (Str) word that the entropy is being calculated on, based on remaining_words
    #     - game_state: (not used)
    def calculate_entropy(self, word, game_state) -> float:
        #initialize wordCount, entropy and single word array that contains a dictionary with letter and state
        entropy = 0.0
        wordCount = 0
        probability = 0.0
        information = 0.0
        state_word = [{ "letter": word[0],  "state": LetterState.Empty},
                       { "letter": word[1],  "state": LetterState.Empty},
                       { "letter": word[2],  "state": LetterState.Empty},
                       { "letter": word[3],  "state": LetterState.Empty},
                       { "letter": word[4],  "state": LetterState.Empty}
                      ]
                      
        #iterate over each possible state that the word can have
        #for each state, find out how many words would be left in remainingwords
        #then calculate p(x) * log base 2 (1/p(x)) and add it to entropy
        # p(x) = possible_matches_with_state / len(remaining words)
        #ie: "for state in range(0,243)"
        for state1 in range(0,3):
            for state2 in range(0,3):
                for state3 in range(0,3):
                    for state4 in range(0,3):
                        for state5 in range(0,3):
                            #initialize to next possible state
                            state_word[0]["state"] = LetterState(state1)
                            state_word[1]["state"] = LetterState(state2)
                            state_word[2]["state"] = LetterState(state3)
                            state_word[3]["state"] = LetterState(state4)
                            state_word[4]["state"] = LetterState(state5)

                            
                            #go over remaining words and if they fit under the current state, add 1 to wordcount
                            #this for loop is calculating the numerator for our p(x)
                            for remaining_word in remaining_words:
                                #-------------------------------------------
                                #if our state says a certain letter is not in
                                #the answer word (ie: LetterState = Empty), then if the remaining_word
                                #contains that letter, we dont include the word in wordCount

                                #(LetterState = Empty)
                                if(state_word[0]["state"] == LetterState.Empty):
                                    if(state_word[0]["letter"] in remaining_word):
                                        continue
                                if(state_word[1]["state"] == LetterState.Empty):
                                    if(state_word[1]["letter"] in remaining_word):
                                        continue
                                if(state_word[2]["state"] == LetterState.Empty):
                                    if(state_word[2]["letter"] in remaining_word):
                                        continue
                                if(state_word[3]["state"] == LetterState.Empty):
                                    if(state_word[3]["letter"] in remaining_word):
                                        continue
                                if(state_word[4]["state"] == LetterState.Empty):
                                    if(state_word[4]["letter"] in remaining_word):
                                        continue
                                #-------------------------------------------
                                #our state says our answer word contains the letter,
                                #just not in the current location (ie: LetterState = Yellow)
                                #so if the word contains the letter in that location
                                #continue, or if the letter is not in the word
                                #altogether then continue

                                #(LetterState = Yellow)
                                if(state_word[0]["state"] == LetterState.Yellow):
                                    if(remaining_word[0] == state_word[0]["letter"]):
                                        continue
                                    if(not state_word[0]["letter"] in remaining_word):
                                        continue
                                if(state_word[1]["state"] == LetterState.Yellow):
                                    if(remaining_word[1] == state_word[1]["letter"]):
                                        continue
                                    if(not state_word[1]["letter"] in remaining_word):
                                        continue
                                if(state_word[2]["state"] == LetterState.Yellow):
                                    if(remaining_word[2] == state_word[2]["letter"]):
                                        continue
                                    if(not state_word[2]["letter"] in remaining_word):
                                        continue
                                if(state_word[3]["state"] == LetterState.Yellow):
                                    if(remaining_word[3] == state_word[3]["letter"]):
                                        continue
                                    if(not state_word[3]["letter"] in remaining_word):
                                        continue
                                if(state_word[4]["state"] == LetterState.Yellow):
                                    if(remaining_word[4] == state_word[4]["letter"]):
                                        continue
                                    if(not state_word[4]["letter"] in remaining_word):
                                        continue
                                #-------------------------------------------
                                #our state says that the letter is in the correct
                                #position(ie: LetterState = Green), so we check if the word has the letter
                                #in the correct position, and if not continue

                                #(LetterState = Green)
                                if(state_word[0]["state"] == LetterState.Green):
                                    if(not remaining_word[0] == state_word[0]["letter"]):
                                        continue
                                if(state_word[1]["state"] == LetterState.Green):
                                    if(not remaining_word[1] == state_word[1]["letter"]):
                                        continue
                                if(state_word[2]["state"] == LetterState.Green):
                                    if(not remaining_word[2] == state_word[2]["letter"]):
                                        continue
                                if(state_word[3]["state"] == LetterState.Green):
                                    if(not remaining_word[3] == state_word[3]["letter"]):
                                        continue
                                if(state_word[4]["state"] == LetterState.Green):
                                    if(not remaining_word[4] == state_word[4]["letter"]):
                                        continue
                                #if we make it to this point, then the remaining_word from remaining_words is a possibility for that state
                                #so we increase wordcount
                                wordCount += 1

                            #calculate the probability for this given state
                            probability = (wordCount/len(remaining_words))
                            #in the case probability is 0, just continue
                            if(probability == 0):
                               continue
                            #calculate the information and add it to entropy
                            information = (probability) * (math.log2(1/probability))
                            entropy = entropy + information

                            #reset word count
                            wordCount = 0
        return entropy

