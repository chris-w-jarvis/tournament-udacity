#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

# THIS WORKS JUST NEED TO FIX FINAL OUTPUT

import psycopg2
import re

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournaments")
    

def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    query = 'DELETE FROM matches;'
    c.execute(query)
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    query = 'DELETE FROM players;'
    c.execute(query)
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    query = 'SELECT COUNT(id) FROM players;'
    c.execute(query)
    result = c.fetchall()[0][0]
    db.close()
    return result

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    query = "INSERT INTO players VALUES (DEFAULT, %s,0,0);"
    data = (name,)
    c.execute(query,data)
    db.commit()
    db.close()

def initializeTourney(number_of_entrants):
    db = connect()
    c = db.cursor()
    number_of_entrants = int(number_of_entrants)
    c.execute('INSERT INTO tournaments VALUES (DEFAULT, %d,NULL);',(number_of_entrants,))
    db.commit()
    db.close()

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
    db = connect()
    c = db.cursor()
    query = 'SELECT * FROM players ORDER BY wins DESC;'
    c.execute(query)
    result = c.fetchall()
    db.close()
    return result

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    c.execute('UPDATE players SET wins = wins + 1, '
    'matches_played = matches_played + 1 WHERE id = %s;',(winner,))
    c.execute('UPDATE players SET matches_played = matches_played + 1 WHERE'
    ' id = %s;',(loser,)) 
    db.commit()

    # report to matches table
    c.execute('INSERT INTO matches VALUES (DEFAULT, %s, %s, NULL)',(winner,loser,))
    db.commit()
    db.close()
 
def swissPairings():
    
    # this is designed to work for odd numbers as well, giving the odd team out
    # a bye week and points equivalent to a win
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
    db = connect()
    c = db.cursor()
    c.execute('SELECT id, name FROM ordered_players;')
    results = c.fetchall()
    match_list = []
    for row1, row2 in results[::2]:
        if row2:
            match_list.append((row1,row2))
        '''else:
            row1 = str(row1)
            match_list.append(('%s has bye' % (row1)))'''
    print match_list
    return match_list
    
swissPairings()
