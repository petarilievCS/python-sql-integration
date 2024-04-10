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


def main(db):
    if len(sys.argv) != 2:
        print(USAGE)
        return 1

    pokemon_name = sys.argv[1]

    # TODO: your code here


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
