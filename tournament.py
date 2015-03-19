#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from contextlib import closing


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament user=vagrant")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cur = conn.cursor()
    SQL = "DELETE FROM matches;"
    cur.execute(SQL)
    conn.commit()
    
    cur.close()
    conn.close()

    return True


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cur = conn.cursor()
    SQL = "DELETE FROM players;"
    cur.execute(SQL)
    conn.commit()
    
    cur.close()
    conn.close()

    return True


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cur = conn.cursor()
    SQL = "SELECT count(*) FROM players;"
    cur.execute(SQL)
    result = cur.fetchone()
    
    cur.close()
    conn.close()

    return result[0]



def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cur = conn.cursor()
    SQL = "INSERT INTO players(name) VALUES(%s);"
    data = (name, )
    cur.execute(SQL, data)
    conn.commit()
    
    cur.close()
    conn.close()

    return True


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cur = conn.cursor()
    p_SQL = "SELECT * FROM players;"
    cur.execute(p_SQL)
    players = cur.fetchall()
    results = []
    for p in players:
        SQL = "SELECT count(*) FROM matches where win_id=%s"
        cur.execute(SQL, (p[0],))
        w = cur.fetchone()
        SQL = "SELECT count(*) FROM matches where loss_id=%s"
        cur.execute(SQL, (p[0],))
        l = cur.fetchone()
        results.append((p[0], p[1], int(w[0]), int(w[0])+int(l[0])))

    cur.close()
    conn.close()
    
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cur = conn.cursor()
    SQL = "INSERT INTO matches(win_id, loss_id) VALUES(%s, %s);"
    data = (int(winner), int(loser) )
    cur.execute(SQL, data)
    conn.commit()
    
    cur.close()
    conn.close()

    return True
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    cur = conn.cursor()
    # use the W/L view to define the pairs
    p_SQL = "SELECT * FROM player_w_l;"
    cur.execute(p_SQL)
    players = cur.fetchall()
    results = []
    for p in players:
        won = int(p[2])
        games = int(p[2])+int(p[3])
        results.append((p[0], p[1], won/games))

    cur.close()
    conn.close()
    ordered = sorted(results, key=lambda x: x[2], reverse=True)
    results = []
    for i, r in enumerate(ordered):
        if i % 2 == 0:
            results.append((r[0], r[1], ordered[i+1][0], ordered[i+1][1]))

    return results


