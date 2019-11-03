# CapitalOne_MindSumo
Repo for Capital One Mind Sumo Challenge

Link: http://mindsumo-jeopardy.herokuapp.com/

#### Stack For Application
* Python
* Flask
* Postgres DB with SQLAlchemy
* Hosted on Heroku

#### Features
* ##### All 18,000 Categories Index
 * Search By Title
 * Search By Point Values
 * Search Through a Date Range
 * Pagination returns pages of matching queries

* ##### User Account System
 * Allows User to Save Favorites From Question Search
 * Questions are linked and specfic to the user account
 * Register for new Accounts
 
* ##### Jeopardy Board
 * Full Board Game Simulation
 * Allows User to Add Multiple Categories to Be Considerd For Game
 * Finds Categories with Matching Titles and filters through valid game boards
 * Corresponding Point Values For the Question
 * Same Category Can Result in DIfferent Questions because it randomizes from searching the valid question for the point value
 * Clue is disabled after view for each session, to keep track of already answered questions
 
* ##### View Favorites
 * Allows User to View Favorites specific to account
 * Questions can be saved from the Search Results
 


