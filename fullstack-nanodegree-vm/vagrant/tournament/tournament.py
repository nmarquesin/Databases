#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    # Connect to database
    conn = connect()

    # Open a cursor to perform database operations
    c = conn.cursor()

    # Delete from matches table
    c.execute("DELETE FROM matches;")

    # Delete from players table
    c.execute("UPDATE players SET wins = %s, matches = %s;", (0, 0))

    # Make changes to database
    conn.commit()

    # Close connection
    c.close()
    conn.close()

    return 0


def deletePlayers():
    """Remove all the player records from the database."""
    # Connect to database
    conn = connect()

    # Open a cursor to perform database operations
    c = conn.cursor()

    c.execute("DELETE FROM players;")

    # Make changes to database
    conn.commit()

    # Close connection
    c.close()
    conn.close()

    return 0


def countPlayers():
    """Returns the number of players currently registered."""
    # Connect to database
    conn = connect()

    # Open a cursor to perform database operations
    c = conn.cursor()

    c.execute("SELECT COUNT(name) FROM players;")
    total = c.fetchone()

    # Close connection
    c.close()
    conn.close()

    return total[0]


def registerPlayer(fullName):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    # Connect to database
    conn = connect()

    # Open a cursor to perform database operations
    c = conn.cursor()

    c.execute("INSERT INTO players (name, wins, matches) VALUES (%s,%s,%s);", (fullName, 0, 0))

    # Make changes to database
    conn.commit()

    # Debug lines
    print(fullName+" was added to the table")
    c.execute("SELECT * FROM players;")

    # Close connection
    c.close()
    conn.close()
    return 0


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
    # Open connection
    conn = connect()

    # Create cursor
    c = conn.cursor()

    # Perform queries
    c.execute("SELECT * FROM players ORDER BY wins DESC;")
    standings = c.fetchall()

    # Close connection
    c.close()
    conn.close()

    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # Open connection
    conn = connect()

    # Create cursor
    c = conn.cursor()

    # Perform INSERT
    if (winner < loser):
        player1 = winner
        player2 = loser
    else:
        player2 = winner
        player1 = loser

    c.execute("INSERT INTO matches VALUES (%s, %s, %s);",(player1, player2, winner,))
    c.execute("SELECT * FROM matches;")
    matchesTable = c.fetchall()

    # Update players table for winner
    c.execute("SELECT wins, matches from players WHERE id = %s;", [winner])
    oldStats = c.fetchone()
    victories = oldStats[0] + 1

    rounds = oldStats[1] + 1
    c.execute("UPDATE players SET wins = %s, matches = %s WHERE id = %s;", (victories, rounds, winner))

    # Update players table for loser
    c.execute("SELECT matches from players WHERE id = %s;", [loser])
    oldStat = c.fetchone()
    rounds = oldStat[0] + 1
    c.execute("UPDATE players SET matches =%s WHERE id = %s;", (rounds, loser,))

    # Commit changes
    conn.commit()

    # Close connection
    c.close()
    conn.close()

    return 0


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
    allPlayers = playerStandings()
    print("A list of all players:")
    print(allPlayers)
    count = 0
    pairs = []
    for i in allPlayers:
        if count % 2 == 0:
            pairs += [(allPlayers[count][0],allPlayers[count][1],allPlayers[count+1][0],allPlayers[count+1][1])]
        count += 1
    return pairs
