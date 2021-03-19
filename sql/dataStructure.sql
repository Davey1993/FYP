CREATE DATABASE footballPrediction;
USE footballPrediction;

DROP TABLE IF EXISTS premierLeague;

CREATE TABLE premierLeague (
   teamId INTEGER NOT NULL PRIMARY KEY,
   teamName varchar(255) NOT NULL,
   teamHomeWins INTEGER NOT NULL,
   teamHomeDraws INTEGER NOT NULL,
   teamHomeLosses INTEGER NOT NULL,
   teamAwayWins INTEGER NOT NULL,
   teamAwayDraws INTEGER NOT NULL,
   teamAwayLosses INTEGER NOT NULL,
   goalsForHome INTEGER NOT NULL,
   goalsForAway INTEGER NOT NULL,
   goalsConcededHome INTEGER NOT NULL,
   goalsConcededAway INTEGER NOT NULL
   );
   
INSERT INTO premierLeague (teamId,teamName,teamHomeWins,teamHomeDraws,teamHomeLosses,teamAwayWins,teamAwayDraws,teamAwayLosses,goalsForHome,goalsForAway,goalsConcededHome,goalsConcededAway) VALUES (33,"Manchester United",3,2,1,3,2,1,2,3,1,2);
   
 DROP TABLE IF EXISTS bundesliga;
 CREATE TABLE bundesliga (
   teamId INTEGER NOT NULL PRIMARY KEY,
   teamName varchar(255) NOT NULL,
   teamHomeWins INTEGER NOT NULL,
   teamHomeDraws INTEGER NOT NULL,
   teamHomeLosses INTEGER NOT NULL,
   teamAwayWins INTEGER NOT NULL,
   teamAwayDraws INTEGER NOT NULL,
   teamAwayLosses INTEGER NOT NULL,
   goalsForHome INTEGER NOT NULL,
   goalsForAway INTEGER NOT NULL,
   goalsConcededHome INTEGER NOT NULL,
   goalsConcededAway INTEGER NOT NULL
   ); 
   
   DROP TABLE IF EXISTS spanishLeague;
   CREATE TABLE spanishLeague (
   teamId INTEGER  NOT NULL PRIMARY KEY,
   teamName varchar(255) NOT NULL,
   teamHomeWins INTEGER NOT NULL,
   teamHomeDraws INTEGER NOT NULL,
   teamHomeLosses INTEGER NOT NULL,
   teamAwayWins INTEGER NOT NULL,
   teamAwayDraws INTEGER NOT NULL,
   teamAwayLosses INTEGER NOT NULL,
   goalsForHome INTEGER NOT NULL,
   goalsForAway INTEGER NOT NULL,
   goalsConcededHome INTEGER NOT NULL,
   goalsConcededAway INTEGER NOT NULL
   );
   
