#! /usr/bin/env python3


"""
COMP3311
24T1
Assignment 2
Pokemon Database

Written by: Petar Iliev z5567169
Written on: 18/4/2024

File Name: Q2

Description: List all locations where a specific pokemon can be found
"""


import sys
import psycopg2
import helpers


### Constants
USAGE = f"Usage: {sys.argv[0]} <pokemon_name>"

query = '''
    SELECT DISTINCT game, location, rarity, minLevel, maxLevel, requirements, region
    FROM Q2
    WHERE pokemon = %s
    ORDER BY region, game, location, rarity, minLevel, maxLevel, requirements;
'''

def main(db):
    if len(sys.argv) != 2:
        print(USAGE)
        return 1

    pokemon_name = sys.argv[1]
    cur = db.cursor()

    if not helpers.pokemon_exists(pokemon_name, cur):
        print(f"Pokemon \"{pokemon_name}\" does not exist")
        return 

    cur.execute(query, [helpers.clean(pokemon_name)])
    result = cur.fetchall()
    
    # Check if encounters exist
    if len(result) == 0:
        print(f"Pokemon \"{pokemon_name}\" is not encounterable in any game")
        return
    
    # Find longest entry for each attribute
    len1, len2, len3, len6 = find_attribute_lengths(result)

    # Check if additional whitespace is needed
    diff1 = len1 - len("Game")
    diff2 = len2 - len("Location")
    diff3 = len3 - len("Rarity")
    print("Game " + diff1 * " " + "Location " + diff2 * " " + "Rarity " + diff3 * " " + "MinLevel MaxLevel " + "Requirements")

    for tuple in result:
        game, location, rarity, min_level, max_level, requirements = tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5]
        print(f"{game:<{len1}} {location:<{len2}} {rarity:<{len3}} {min_level:<8} {max_level:<8} {requirements}")

def find_attribute_lengths(result):
    len1, len2, len3, len6 = len('Game'), len('Location'), len('Rarity'), len('Requirements')
    for tuple in result:
        game, location, rarity, requirements = tuple[0], tuple[1], tuple[2], tuple[5]

        if len(game) > len1: len1 = len(game)
        if len(location) > len2: len2 = len(location)
        if len(rarity) > len3: len3 = len(rarity)
        if len(requirements) > len6: len6 = len(requirements)
    
    return len1, len2, len3, len6

if __name__ == '__main__':
    exit_code = 0
    try:
        db = psycopg2.connect(dbname="pkmon")
        exit_code = main(db)
    except psycopg2.Error as err:
        print("DB error: ", err)
        exit_code = 1
    except Exception as err:
        print("Internal Error: ", err)
        raise err
    finally:
        if db is not None:
            db.close()
    sys.exit(exit_code)
