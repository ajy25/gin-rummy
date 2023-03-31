import mysql.connector


class DBOperator:

    cursor = None
    db_name: str = None
    cardtable_name: str = None
    scoretable_name: str = None

    def __init__(self, cursor, db_name: str = None, \
                 cardtable_name: str = None, \
                    scoretable_name: str = None) -> None:
        self.cursor = cursor
        if db_name:
            self.db_name = db_name
        if cardtable_name:
            self.cardtable_name = cardtable_name
        if scoretable_name:
            self.scoretable_name = scoretable_name
        if db_name and cardtable_name and scoretable_name:
            self.setup_tables()

    def make_db(self, db_name: str = None) -> bool:
        '''Attempts to create a database given a database name. Returns false
        if the database already exists, true otherwise.'''
        if not db_name:
            db_name = self.db_name

        try:
            self.cursor.execute(f"CREATE DATABASE {db_name};")
            return True
        except:
            return False

    def make_cards_table(self, table_name: str = None, \
                         db_name: str = None) -> bool:
        '''Makes a table with columns gameID, val, suit, pile, scoretype, 
        and stackorder. Returns true if successful, false otherwise.'''
        if not db_name:
            db_name = self.db_name
        if not table_name:
            table_name = self.cardtable_name

        try:
            self.cursor.execute(f"USE {db_name};")
            self.cursor.execute(f"CREATE TABLE {table_name} " + \
                "(gameID int NOT NULL, val varchar(255) NOT NULL, " + \
                "suit varchar(255) NOT NULL, pile varchar(255) NOT NULL, " + \
                "scoretype varchar(255), stackorder int NOT NULL);")
            return True
        except:
            return False

    def make_scores_table(self, table_name: str = None, db_name: str = None) \
        -> bool:
        '''Makes a table with columns gameID, p1, p2, and roundnum. 
        Returns true if successful, false otherwise.'''
        if not db_name:
            db_name = self.db_name
        if not table_name:
            table_name = self.scoretable_name

        try:
            self.cursor.execute(f"USE {db_name};")
            self.cursor.execute(f"CREATE TABLE {table_name} " + \
                "(gameID int NOT NULL, p1 int NOT NULL, p2 int NOT NULL, " + \
                "roundnum int NOT NULL);")
            return True
        except:
            return False

    def setup_tables(self, db_name: str = None, cardtable_name: str = None, \
                     scoretable_name: str = None):
        '''Sets up necessary database and tables for Gin Rummy'''
        if not db_name:
            db_name = self.db_name
        if not cardtable_name:
            cardtable_name = self.cardtable_name
        if not scoretable_name:
            scoretable_name = self.scoretable_name

        self.make_db(db_name)
        self.make_cards_table(cardtable_name)
        self.make_scores_table(scoretable_name)

    def print_tables(self, db_name: str = None):
        if not db_name:
            db_name = self.db_name

        self.cursor.execute(f"USE {db_name};")
        self.cursor.execute("SHOW TABLES;")
        c = list(self.cursor.fetchall())

        for x in c:
            print(x)
        print('')

    def print_rows(self, table_name: str, db_name: str = None):
        if not db_name:
            db_name = self.db_name

        self.cursor.execute(f"USE {db_name};")
        self.cursor.execute(f"SELECT * FROM {table_name};")
        c = list(self.cursor.fetchall())

        for x in c:
            print(x)
        print('')

    def print_db(self):
        self.cursor.execute("SHOW DATABASES;")
        c = list(self.cursor)

        for x in c:
            print(x)
        print('')

    def clean_db(self, db_name_contains: str):
        self.cursor.execute("SHOW DATABASES;")
        c = list(self.cursor)

        for x in c:
            if db_name_contains in str(x[0]):
                self.cursor.execute(f"DROP DATABASE {x[0]};")

    def gameID_in_table(self, gameID: int, table_name: str, \
                        db_name: str = None) -> bool:
        '''Returns true if gameID is in the table. Otherwise, returns false.
        '''
        if not db_name:
            db_name = self.db_name

        self.cursor.execute(f"USE {db_name};")
        self.cursor.execute(f"SELECT * FROM {table_name} WHERE gameID={gameID};")
        c = list(self.cursor)
        if len(c) == 0:
            return False
        else:
            return True

    def delete_rows_with_gameID(self, gameID: int, table_name: str, \
                                db_name: str = None):
        if not db_name:
            db_name = self.db_name

        self.cursor.execute(f"USE {db_name};")
        self.cursor.execute(f"DELETE FROM {table_name} WHERE gameID={gameID};")

