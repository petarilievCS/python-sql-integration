#! /usr/bin/env python3


"""
COMP3311
24T1
Assignment 2
Pokemon Database

Written by: Petar Iliev z5567169
Written on: 15/04/2024

File Name: Q5

Description: Print a formatted (recursive) evolution chain for a given pokemon
"""


import sys
import psycopg2
import helpers


### Constants
USAGE = f"Usage: {sys.argv[0]} <pokemon_name>"

### Queries
pre_evolution_query = '''
    SELECT DISTINCT pre.name, pre.id
    FROM Evolutions e
    JOIN Pokemon post ON (e.post_evolution = post.id)
    JOIN Pokemon pre ON (e.pre_evolution = pre.id)
    WHERE post.name = %s
    ORDER BY pre.id;
'''

post_evolution_query = '''
    SELECT DISTINCT post.name, post.id
    FROM Evolutions e
    JOIN Pokemon pre ON (e.pre_evolution = pre.id)
    JOIN Pokemon post ON (e.post_evolution = post.id)
    WHERE pre.name = %s
    ORDER BY post.id;
'''

evolutions_query = '''
    SELECT e.id 
    FROM Evolutions e
    JOIN Pokemon pre ON (e.pre_evolution = pre.id)
    JOIN Pokemon post ON (e.post_evolution = post.id)
    WHERE pre.name = %s AND post.name = %s;
'''

requirement_query = '''
    SELECT r.assertion, er.inverted
    FROM Evolutions e
    JOIN Evolution_Requirements er ON (e.id = er.evolution)
    JOIN Requirements r ON (er.requirement = r.id)
    WHERE er.evolution = %s
    ORDER BY er.inverted, r.id;
'''

def main(db):
    if len(sys.argv) != 2:
        print(USAGE)
        return 1

    pokemon_name = sys.argv[1]
    
    # TODO: your code here
    cur = db.cursor()

    # Input check
    if not helpers.pokemon_exists(pokemon_name, cur):
        return 

    pre_evolution(pokemon_name, cur)
    post_evolution(pokemon_name, cur)

def pre_evolution(pokemon, cur):
    cur.execute(pre_evolution_query, [pokemon])
    result = cur.fetchall()
    
    # Base case
    if len(result) == 0:
        print()
        print(f"'{pokemon}' doesn't have any pre-evolutions.")
        return

    # Recursive case
    for tuple in result:
        pre_pokemon = tuple[0]
        print()
        print(f"'{pokemon}' can evolve from '{pre_pokemon}' when the following requirements are satisfied:")

        cur.execute(evolutions_query, [pre_pokemon, pokemon])
        evolutions = cur.fetchall()
        print_evolutions(evolutions, cur)
        pre_evolution(pre_pokemon, cur)

def post_evolution(pokemon, cur):
    cur.execute(post_evolution_query, [pokemon])
    result = cur.fetchall()
    
    # Base case
    if len(result) == 0:
        print()
        print(f"'{pokemon}' doesn't have any post-evolutions.")
        return

    # Recursive case
    for tuple in result:
        post_pokemon = tuple[0]
        print()
        print(f"'{pokemon}' can evolve into '{post_pokemon}' when the following requirements are satisfied:")

        cur.execute(evolutions_query, [pokemon, post_pokemon])
        evolutions = cur.fetchall()
        print_evolutions(evolutions, cur)

        post_evolution(post_pokemon, cur)

def print_evolutions(evolutions, cur):

    if len(evolutions) == 1:
        print_evolution(evolutions[0], cur, 1)

    else:
        print_evolution(evolutions[0], cur, 2)
        for evolution in evolutions[1:]:
            print("\tOR")
            print_evolution(evolution, cur, 2)

def print_evolution(evolution, cur, num_tabs):
    cur.execute(requirement_query, [evolution])
    result = cur.fetchall()

    # Only 1 requirement
    if len(result) == 1:
        print_requirement(result[0][0], result[0][1], num_tabs)

    else:
        print_requirement(result[0][0], result[0][1], num_tabs + 1)
        for i in range(1, len(result)):
            tuple = result[i]
            assertion, inverted = tuple[0], tuple[1]
            print(num_tabs * "\t" + "AND")
            print_requirement(assertion, inverted, num_tabs + 1)

def print_requirement(assertion, inverted, num_tabs):
    if inverted:
        assertion = "NOT " + assertion
    statement = num_tabs * "\t" + assertion
    print(statement)

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
