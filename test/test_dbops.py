import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f'{dir_path}/../')

import mysql.connector
from src.db_ops import DBOperator
from src.game import Game


# SQL Server Information
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sbds1234"
)
cursor = db.cursor(buffered=True)

def test_db():
    db_op = DBOperator(cursor, 'test_sql', 'ginrummycards', 'ginrummyscores')

    db_op.clean_db('test_sql')
    db_op.print_db()

    # sets up necessary empty tables
    db_op.setup_tables()

    db_op.print_db()
    db_op.print_tables()

    g1 = Game(db_op.cursor, 20, 'test_sql', 'ginrummycards', 'ginrummyscores')
    g2 = Game(db_op.cursor, 30, 'test_sql', 'ginrummycards', 'ginrummyscores')

    print(db_op.gameID_in_table(20, 'ginrummycards'))
    db_op.print_rows('ginrummycards')
    db_op.print_rows('ginrummyscores')

    db_op.delete_rows_with_gameID(20, 'ginrummycards')
    db_op.delete_rows_with_gameID(20, 'ginrummyscores')

    print("After removal")
    print(db_op.gameID_in_table(20, 'ginrummycards'))
    db_op.print_rows('ginrummycards')
    db_op.print_rows('ginrummyscores')

if __name__ == '__main__':
    test_db()





