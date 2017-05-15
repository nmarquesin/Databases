-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE players(
  id serial primary key,
  name varchar(50),
  wins integer,
  matches integer
);

CREATE TABLE matches(
  player1 integer REFERENCES players,
  player2 integer REFERENCES players,
  winner integer REFERENCES players
);
