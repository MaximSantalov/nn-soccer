import sqlite3

# following the example of python docs given here
# https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.row_factor
def dict_factory (cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class Fetcher:
    def __init__ (self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.conn.row_factory = dict_factory

    # returns a tuple (player, player_attrs)
    # `player` is a dictionary containing the row from the Player table
    # `player_attrs` is list of dictionaries, each dictionary is the
    # row from the Player_Attributes for the player with given api_id
    # (each player has many such entries in the dictionary)
    def get_player_data (self, api_id):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM Player WHERE player_api_id=?", (api_id,))
        player = cur.fetchone()
        cur.execute("SELECT * FROM Player_Attributes WHERE player_api_id=?", (api_id,))
        player_attrs = cur.fetchall()
        return (player, player_attrs)

"""
fetcher = Fetcher("data/database.sqlite")
(player, attrs) = fetcher.get_player_data(505942)
print(player)
print()
print()
for row in attrs:
    print(row)
    print()
    print()
"""
