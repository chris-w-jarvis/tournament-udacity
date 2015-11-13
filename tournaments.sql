-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE table players(
id serial PRIMARY KEY,
 name text,
 wins int,
 matches_played int);

CREATE table tournaments(
id serial PRIMARY KEY,
 number_entrants int,
 winner int REFERENCES players (id));

CREATE table matches(
match_id serial PRIMARY KEY,
 player1 int REFERENCES players (id),
 player2 int REFERENCES players (id),
 tournament_id int REFERENCES tournaments (id));

CREATE VIEW ordered_players AS SELECT id, name FROM
 players ORDER BY wins DESC;

CREATE VIEW ordered_players_display AS
 SELECT a.id, b.id FROM
 ordered_players AS a, ordered_players AS b
 WHERE a.id != b.id;

