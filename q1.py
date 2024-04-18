#! /usr/bin/env python3


"""
COMP3311
24T1
Assignment 2
Pokemon Database

Written by: Petar Iliev z5567169
Written on: 10/04/2024

File Name: Q1.py

Description: List the number of pokemon and the number of locations in each game
"""


import sys
import psycopg2
import helpers


### Constants
USAGE = f"Usage: {sys.argv[0]}"

### Queries
query = '''
    SELECT 
        g.region,
        g.name, 
        COUNT(DISTINCT p.national_id), 
        COUNT(DISTINCT l.name)
    FROM Games g
    JOIN Pokedex p ON p.game = g.id
    JOIN Locations l ON l.appears_in = g.id
    GROUP BY g.region, g.name;
'''

def main(db):
    if len(sys.argv) != 1:
        print(USAGE)
        return 1
    
    cur = db.cursor()
    cur.execute(query)
    result = cur.fetchall()

    print('Region Game              #Pokemon #Locations')
    for tuple in result:
        region, game, pokemon_num, location_num = tuple[0], tuple[1], tuple[2], tuple[3]
        print(f"{region:<6} {game:<17} {pokemon_num:<8} {location_num:<10}")

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
