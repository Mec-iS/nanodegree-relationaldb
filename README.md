# nanodegree-relationaldb

## Project 2: SQL database with PostGRE
The task is about designing an implementing in Python2.7 a database to handle a round-robin tournament with Swiss-pairing:

<pre>The goal of the Swiss pairings system is to pair each player with an opponent who has won the same number of matches, or as close as possible.

You can assume that the number of players in a tournament is an even number. This means that no player will be left out of a round.</pre>

The database schema is in `tournament.sql`. Python code is in `tournament.py`. Tests are in `tournament_test.py`.


### Building the DB:

You need `PostGRESQL >= 9.1` and `Python 2.7` installed in your system.


- Install `psycopg2` in your Python interpreter:

`$ pip install psycopg2`

- Git clone this repository:

`$ git clone https://github.com/Mec-iS/nanodegree-relationaldb`

- Connect to your PostGRE instance from the directory where the repo got cloned:

`$ psql`

- Run database schema creation:

`$ db=> \i tournament.sql`

- Run tests for the scripts:

`$ python tournament_test.py`

- Check what got stored in the database, from your command line:

`$ psql` 

- From the PostGRE command line

`$ db=> \c tournament`


- Then

`$ tournament=> SELECT * FROM players;`

- and

`$ tournament=> SELECT * FROM matches;`

