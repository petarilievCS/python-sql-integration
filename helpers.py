# COMP3311 23T1 Assignment 2 ... Python helper functions
# add any functions to share between Python scripts

import re

### Queries 
pokemon_query = '''
    SELECT COUNT(*)
    FROM Pokemon
    WHERE name = %s;
'''

def clean(s: str) -> str:
    """
    Clean user input
    remove leading and trailing whitespace
    convert to title case (first letter of each word is uppercase, the rest are lowercase)
    squish multiple whitespace characters into a single space
    """
    return re.sub(r'\s+', ' ', s.strip().title())

def pokemon_exists(name, cur):
    cur.execute(pokemon_query, [name])
    result = cur.fetchone()

    if result[0] == 0:
        print(f'Pokemon "{name}" does not exist')
        return False
    return True
    
    