import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f'{dir_path}/../')

import mysql.connector
from src import db_ops
from src.game import Game


def test_db():
    db_ops.clean_db('test_sql')
    db_ops.print_db()

    # sets up necessary empty tables
    db_ops.setup('test_sql', 'ginrummycards', 'ginrummyscores')

    db_ops.print_db()
    db_ops.print_tables('test_sql')

    g1 = Game(db_ops.cursor, 20, 'test_sql', 'ginrummycards', 'ginrummyscores')
    g2 = Game(db_ops.cursor, 30, 'test_sql', 'ginrummycards', 'ginrummyscores')

    db_ops.print_rows('test_sql', 'ginrummycards')
    db_ops.print_rows('test_sql', 'ginrummyscores')

    db_ops.delete_rows_with_gameID('test_sql', 'ginrummycards', 20)
    db_ops.delete_rows_with_gameID('test_sql', 'ginrummyscores', 20)

    print("After removal")
    db_ops.print_rows('test_sql', 'ginrummycards')
    db_ops.print_rows('test_sql', 'ginrummyscores')


# def test_game():
    


if __name__ == '__main__':
    test_db()





