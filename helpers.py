# COMP3311 23T1 Assignment 2 ... Python helper functions
# add any functions to share between Python scripts

import re

def clean(s: str) -> str:
    """
    Clean user input
    remove leading and trailing whitespace
    convert to title case (first letter of each word is uppercase, the rest are lowercase)
    squish multiple whitespace characters into a single space
    """
    return re.sub(r'\s+', ' ', s.strip().title())

def get_rarity_string(rarity: int) -> str:
    """
    Converts rarity to string
    """
    if rarity >= 21:
        return "Common"
    elif rarity >= 6 and rarity <= 20:
        return "Uncommon"
    elif rarity >= 1 and rarity <= 5:
        return "Rare"
    else:
        return "Limited"
    
    