import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(f'{dir_path}/')

import mysql.connector
from src.db_ops import DBOperator

# SQL Server Information
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sbds1234"
)
cursor = db.cursor(buffered=True)

db_name = 'test_sql'
cardtable_name = 'ginrummycards'
scoretable_name = 'ginrummyscores'
db_op = DBOperator(cursor, db_name=db_name, cardtable_name=cardtable_name, 
                   scoretable_name=scoretable_name)

db_op.clean_db('test_sql')
db_op.print_db()