#! /usr/bin/env python3


"""
COMP3311
24T1
Assignment 2
Pokemon Database

Written by: <YOUR NAME HERE> <YOUR STUDENT ID HERE>
Written on: <DATE HERE>

File Name: Q2

Description: List all locations where a specific pokemon can be found
"""


import sys
import psycopg2
import helpers


### Constants
USAGE = f"Usage: {sys.argv[0]} <pokemon_name>"

query = '''
    SELECT g.name, l.name, e.rarity, e.levels, Get_Requirements(e.id)
    FROM Pokemon p
    JOIN Encounters e ON (e.occurs_with = p.id)
    JOIN Locations l ON (e.occurs_at = l.id)
    JOIN Games g ON (l.appears_in = g.id)
    WHERE p.name = %s
    ORDER BY g.region, g.name, l.name, e.rarity, e.levels;
'''

def main(db):
    if len(sys.argv) != 2:
        print(USAGE)
        return 1

    pokemon_name = sys.argv[1]

    # TODO: your code here
    cur = db.cursor()
    cur.execute(query, [helpers.clean(pokemon_name)])
    result = cur.fetchall()
    
    print("Game              Location                   Rarity   MinLevel MaxLevel Requirements")
    for tuple in result:
        game, location, rarity, levels, requirements = tuple[0], tuple[1], tuple[2], tuple[3], tuple[4]

        rarity_str = helpers.get_rarity_string(rarity)
        levels = levels[1:-1].split(',')
        min_level = levels[0]
        max_level = levels[1]
        print(f"{game:<17} {location:<26} {rarity_str:<8} {min_level:<8} {max_level:<12} {requirements}")

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
