import mysql.connector


# SQL Server Information
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sbds1234"
)
cursor = db.cursor(buffered=True)


def make_db(db_name: str) -> bool:
    '''Attempts to create a database given a database name. Returns false
    if the database already exists, true otherwise.'''
    try:
        cursor.execute(f"CREATE DATABASE {db_name};")
        return True
    except:
        return False

def make_cards_table(db_name: str, table_name: str) -> bool:
    '''Makes a table with columns gameID, val, suit, pile, scoretype, 
    and stackorder. Returns true if successful, false otherwise.'''
    try:
        cursor.execute(f"USE {db_name};")
        cursor.execute(f"CREATE TABLE {table_name} " + \
            "(gameID int NOT NULL, val varchar(255) NOT NULL, " + \
            "suit varchar(255) NOT NULL, pile varchar(255) NOT NULL, " + \
            "scoretype varchar(255), stackorder int NOT NULL);")
        return True
    except:
        return False

def make_scores_table(db_name: str, table_name: str):
    '''Makes a table with columns gameID, p1, p2, and roundnum.'''
    try:
        cursor.execute(f"USE {db_name};")
        cursor.execute(f"CREATE TABLE {table_name} " + \
            "(gameID int NOT NULL, p1 int NOT NULL, p2 int NOT NULL, " + \
            "roundnum int NOT NULL);")
    except:
        pass

def setup(db_name: str, cards_table_name: str, scores_table_name: str):
    '''Sets up necessary database and tables for Gin Rummy'''
    make_db(db_name)
    make_cards_table(db_name, cards_table_name)
    make_scores_table(db_name, scores_table_name)

def print_tables(db_name: str):
    cursor.execute(f"USE {db_name};")
    cursor.execute("SHOW TABLES;")
    c = list(cursor.fetchall())

    for x in c:
        print(x)
    print('')

def print_rows(db_name: str, table_name: str):
    cursor.execute(f"USE {db_name};")
    cursor.execute(f"SELECT * FROM {table_name};")
    c = list(cursor.fetchall())

    for x in c:
        print(x)
    print('')

def print_db():
    cursor.execute("SHOW DATABASES;")
    c = list(cursor)

    for x in c:
        print(x)
    print('')

def clean_db(db_name_contains: str):
    cursor.execute("SHOW DATABASES;")
    c = list(cursor)

    for x in c:
        if db_name_contains in str(x[0]):
            cursor.execute(f"DROP DATABASE {x[0]};")

def gameID_in_table(db_name: str, table_name: str, gameID: int) -> bool:
    '''Returns true if gameID is in the table. Otherwise, returns false.
    '''
    cursor.execute(f"USE {db_name};")
    cursor.execute(f"SELECT * FROM {table_name} WHERE gameID={gameID};")
    c = list(cursor)
    if len(c) == 0:
        return False
    else:
        return True

def delete_rows_with_gameID(db_name: str, table_name: str, gameID: int):
    cursor.execute(f"USE {db_name};")
    cursor.execute(f"DELETE FROM {table_name} WHERE gameID={gameID};")

