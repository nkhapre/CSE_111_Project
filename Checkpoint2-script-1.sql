-- Create Tables
CREATE TABLE player (
    p_name         varchar(100) not null,
    p_number       varchar(100) not null,
    p_team         varchar(100) not null,
    p_position     varchar(100) not null,
    p_key   varchar(100) not null,
    p_season varchar(100) not null,
    PRIMARY KEY(p_key)
);
CREATE TABLE coach (
    c_name         varchar(100) not null,
    c_team         varchar(100) not null,
    c_key           varchar(100) not null ,
    c_season varchar(100) not null,
    PRIMARY KEY(c_key)
);

CREATE TABLE team (
    t_name         varchar(100) not null,
    t_city         varchar(100) not null,
    t_conference   varchar(100) not null
);
CREATE TABLE round (
    r_semi        varchar(100) not null,
    r_quarter        varchar(100) not null,
    r_conference        varchar(100) not null,
    r_final        varchar(100) not null,
    r_season varchar(100) not null
);
CREATE TABLE statistics (
   s_playerkey        varchar(100) not null,
   s_ppg              decimal(3,1) not null,
   s_rpg              decimal(3,1) not null,               
   s_apg              decimal(3,1) not null,
   s_series varchar(100) not null,
   s_season           varchar(100) not null
);
CREATE TABLE playoffseries (
    ps_winningteam         varchar(100) not null,
    ps_losingteam          varchar(100) not null,
    ps_round               varchar(100) not null,
    ps_season           varchar(100) not null
    
);
CREATE TABLE records (
    re_playerkey              varchar(100) not null,
    re_statistics          decimal(3,1) not null
);
CREATE TABLE ison (
    i_round                varchar(100) not null,
    i_series        varchar(100) not null,
    i_season         varchar(100) not null       
);
CREATE TABLE playsin(
    pi_team                varchar(100) not null,
    pi_series       varchar(100) not null,
    pi_round           varchar(100) not null,
    pi_season varchar(100) not null,
    PRIMARY KEY (pi_team, pi_series)

);

CREATE TABLE playsfor(
    pf_playerkey               varchar(100) not null,
    pf_team                 varchar(100) not null,
    pf_season varchar(100) not null
);

CREATE TABLE coachedby(
    cb_coachkey            varchar(100) not null,
    cb_playerkey             varchar(100) not null,
    cb_team               varchar(100) not null,
    cb_season varchar(100) not null,
    PRIMARY KEY (cb_coachkey, cb_playerkey)
);

CREATE TABLE wins(
    w_player               varchar(100) not null,
    w_coach                varchar(100) not null,
    w_team                 varchar(100) not null,
    w_playoffseries        varchar(100) not null,
    w_season varchar(100) not null
);
-- 1: Insert a new player

INSERT INTO playsfor (pf_player, pf_team)
VALUES ('Neil Khapre', 'Boston Celtics', '2021');

INSERT INTO statistics (s_playerkey, s_ppg, s_rpg, s_apg, s_season)
VALUES (3, 10.0, 2.5, 4.5, '2021');



-- 2: Insert a new coach for an existent team

UPDATE coach
SET c_name = 'Ian Pagador'
WHERE c_team = 'Milwaukee Bucks'
WHERE c_key = '5'
WHERE c_season = '2021';

-- 3: Insert a new team

INSERT INTO teams (t_name, t_city, t_conference)
VALUES (team_name, city, conference);

-- 4: Update coachedby with a new coach for a team and its players

INSERT INTO coachedby (cb_coach, cb_player, cb_team)
VALUES (coach_name, players[1], team_name),
       (coach_name, players[2], team_name);

-- 5: Update a player's jersey number

UPDATE player
SET p_number = 23
WHERE p_name = 'Anthony Davis';

-- 6: Replace a series in the round table

UPDATE round
SET r_playoffseries = REPLACE(r_playoffseries, old_series, new_series)
WHERE r_round = current_round;

-- 7: Relocate a team to a new city

UPDATE teams
SET t_name = new_team_name
WHERE t_name = old_team_name;

UPDATE player
SET p_team = new_team_name
WHERE p_team = old_team_name;

UPDATE wins
SET w_team = new_team_name
WHERE w_team = old_team_name;

UPDATE coachedby
SET cb_team = new_team_name
WHERE cb_team = old_team_name;

UPDATE playsfor
SET pf_team = new_team_name
WHERE pf_team = old_team_name;

UPDATE round
SET r_playoffseries = REPLACE(r_playoffseries, old_team_name, new_team_name)
WHERE r_playoffseries LIKE '%' + old_team_name + '%';

UPDATE playsin
SET pi_team = new_team_name
WHERE pi_team = old_team_name;

UPDATE records
SET re_team = new_team_name
WHERE re_team = old_team_name;

-- 8: Remove a player from a team

DELETE FROM player
WHERE p_name = 'Player Name';

DELETE FROM playsfor
WHERE pf_player = 'Player Name';

DELETE FROM records
WHERE re_player = 'Player Name';

DELETE FROM coachedby
WHERE cb_player = 'Player Name';

DELETE FROM wins
WHERE w_player LIKE '%Player Name%';

-- 9: Trade players between two teams

UPDATE player
SET p_team = team2
WHERE p_name = player1;

UPDATE player
SET p_team = team1
WHERE p_name = player2;

UPDATE playsfor
SET pf_team = team2
WHERE pf_player = player1;

UPDATE playsfor
SET pf_team = team1
WHERE pf_player = player2;

UPDATE records
SET re_team = team2
WHERE re_player = player1;

UPDATE records
SET re_team = team1
WHERE re_player = player2;

UPDATE wins
SET w_player = player2
WHERE w_player = player1;

UPDATE wins
SET w_player = player1
WHERE w_player = player2;

-- 10: Swap winning and losing team in playoffseries

UPDATE playoffseries
SET 
    ps_winningteam = ps_losingteam,
    ps_losingteam = ps_winningteam
WHERE ps_winningteam = winning_team;


-- 11: Remove a team

DELETE FROM playsfor
WHERE pf_team = 'New York Knicks';

DELETE FROM wins
WHERE w_team = 'New York Knicks';

DELETE FROM coachedby
WHERE cb_team = 'New York Knicks';

DELETE FROM player
WHERE p_team = 'New York Knicks';

DELETE FROM playoffseries
WHERE ps_winningteam = 'New York Knicks';

DELETE FROM team
WHERE team_name = 'New York Knicks';

-- 12: Retrieve all data regarding a player, combining the player and statistics tables

SELECT *
FROM statistics
NATURAL JOIN player;

-- 13: Retrieve statistics of a certain player

SELECT p_name, s_ppg, s_rpg, s_apg
FROM statistics
NATURAL JOIN player
WHERE p_name = input_name;

-- 14: Retrieve the coach of a certain player

SELECT p_name, c_name
FROM coach
WHERE c_players LIKE '%LeBron James%';

-- 15: Retrieve all playoff series a certain player plays in

SELECT p_name, pi_playoffseries
FROM playsin
JOIN player ON p_team = pi_team
WHERE p_name = 'Joel Embiid';

-- 16: Retrieve all winning teams of the Eastern conference

SELECT DISTINCT(ps_winningteam)
FROM playoffseries
WHERE ps_round LIKE '%Eastern%';

-- 17: Remove a playoff series from the wins table

UPDATE wins
SET w_playoffseries = REPLACE(w_playoffseries, 'Atlanta Hawks vs. Philadelphia 76ers', '')
WHERE w_playoffseries LIKE '%Atlanta Hawks vs. Philadelphia 76ers%';

-- 18: List all teams that participated in a certain round

SELECT GROUP_CONCAT(DISTINCT team ORDER BY team) AS teams_in_western_quarterfinals
FROM (
    SELECT ps_winningteam AS team
    FROM playoffseries
    WHERE ps_round = 'Western Quarterfinals'
    UNION
    SELECT ps_losingteam AS team
    FROM playoffseries
    WHERE ps_round = 'Western Quarterfinals'
) AS combined_teams;

--19. Cities that have won the finals
SELECT t_city
FROM team
JOIN playoffseries
WHERE team.t_name = playoffseries.ps_winningteam
AND playoffseries.ps_round = "NBA Finals"

--20. Select every player's rebounds
SELECT player.p_name AS name, statistics.s_rpg AS rebounds
FROM player
JOIN statistics ON statistics.s_playerkey = player.p_key 
