#! /usr/bin/env python3


"""
COMP3311
24T1
Assignment 2
Pokemon Database

Written by: Petar Iliev z5567169
Written on: 13/04/2024

File Name: Q4

Description: Print the best move a given pokemon can use against a given type in a given game for each level from 1 to 100
"""


import sys
import psycopg2
import helpers


### Constants
USAGE = f"Usage: {sys.argv[0]} <Game> <Attacking Pokemon> <Defending Pokemon>"

### Queries
query = '''
    SELECT name, effectivness, requirements
    FROM Get_Game_Moves(%s, %s, %s)
    ORDER BY effectivness DESC, name;
'''

pokemon_query = '''
    SELECT COUNT(*)
    FROM Pokemon
    WHERE name = %s;
'''

game_query = '''
    SELECT COUNT(*)
    FROM Pokedex px
    JOIN Pokemon pk ON px.national_id = pk.id
    JOIN Games g ON g.id = px.game
    WHERE g.name = %s AND pk.name = %s;
'''

def main(db):
    ### Command-line args
    if len(sys.argv) != 4:
        print(USAGE)
        return 1
    game_name = sys.argv[1]
    attacking_pokemon_name = sys.argv[2]
    defending_pokemon_name = sys.argv[3]

    # TODO: your code here
    cur = db.cursor()

    # Check if Pokemons exist
    for pokemon in [attacking_pokemon_name, defending_pokemon_name]:
        cur.execute(pokemon_query, [pokemon])
        result = cur.fetchone()
        if result[0] == 0:
            print(f"Pokemon \"{pokemon}\" does not exist")
            return
    
    # Check if Pokemons are in game
    for pokemon in [attacking_pokemon_name, defending_pokemon_name]:
        cur.execute(game_query, [game_name, pokemon])
        result = cur.fetchone()
        if result[0] == 0:
            print(f"Pokemon \"{pokemon}\" is not in \"{game_name}\"")
            return

    # Main query
    cur.execute(query, [game_name, attacking_pokemon_name, defending_pokemon_name])
    result = cur.fetchall()
    
    # Check if moves are found
    if len(result) == 0:
        print(f"No moves found for \"{attacking_pokemon_name}\" against \"{defending_pokemon_name}\" in \"{game_name}\"")
        return

    print(f'If \"{attacking_pokemon_name}\" attacks \"{defending_pokemon_name}\" in \"{game_name}\" it\'s available moves are:')

    for tuple in result:
        name, power, requirements = tuple[0], tuple[1], tuple[2]
        print(f"\t{name}")
        print(f"\t\twould have a relative power of {power}")
        print(f"\t\tand can be learnt from {requirements}")


if __name__ == '__main__':
    exit_code = 0
    db = None
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
