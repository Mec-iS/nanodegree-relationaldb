-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;

\c tournament

CREATE TABLE players (
   id SERIAL PRIMARY KEY,
   name VARCHAR(80)
);


CREATE TABLE matches (
   id SERIAL PRIMARY KEY,
   win_id SERIAL references players(id),
   loss_id SERIAL references players(id)
);

CREATE VIEW player_w_l 
   AS SELECT players.id, players.name, 
         (SELECT count(*) FROM matches WHERE win_id=players.id) as win,
         (SELECT count(*) FROM matches WHERE loss_id=players.id) as loss
         FROM players, matches 
         GROUP BY players.id;





