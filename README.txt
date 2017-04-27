Welcome to our CIS422 Development GitHub!

This repo is dedicated to a TeamSort project for sorting 
students into groups in future 422 classes.

Team Members:
Vinitha Gadiraju
Amber Straub
Anisha Aggarwal

---------------------------------------------------------------------
---------------------------------------------------------------------
In order to run our TeamSort, you must have the following apps installed:
PostgreSQL
Python 3

You must also install the packages for the following python libraries:
psycopg2
---------------------------------------------------------------------
You must have PostgreSQL successfully installied, i.e. you can make a
new database with the command line "createdb <dbname>"

This database you make will be an argument to run the TeamSort script.

To install go to:
https://www.postgresql.org/download/

Follow the directions for your system.
---------------------------------------------------------------------
You must have Python 3 successfully installed.
To check if the correct version is installed: python3 -V in the command prompt. 

To install go to:
https://www.python.org/downloads/

Follow directions for your system. 
---------------------------------------------------------------------
You must have psycopg2 successfully installed.

To install go to:
http://initd.org/psycopg/docs/install.html

Follow directions for your system.
---------------------------------------------------------------------
---------------------------------------------------------------------
FEATURES:

Database:
Having a database in the background leads to higher expansibility for future projects and is better for data tracking.

Sorting Algorithm:
4 main criteria: scheduling, strengths, weaknesses, and teammate preference. 

The more well suited a team is for each other, the higher “score” they have. Specifically, the more available times to meet among students in a team, results in a higher score. (ie. If a teammate’s strengths match another teammate’s weaknesses, the score is higher.)
Finally, if a teammate is placed in a group with someone they preferred, the score of the team is higher. 

First, the program randomly assigns students to a team. Then the teams will be shuffled 1000 times with the intent of maximizing team scores to create higher compatibility. After maximizing, the algorithm will output what the new teams are.

GUI Interface:
We decided to be able to read in the user's input on how many groups they would like to have.
We also wanted the user to be able to specify a CSV file if they already had the data instead of forcing them to manually input the data.
---------------------------------------------------------------------
---------------------------------------------------------------------
User Guide:

Open the command line and clone this repository to your machine. You will need a basic understanding of git and command line interfaces to run this program. Verify that all required applications are in fact installed. 

Once you recieve your data back from your students, use Google Poll to download the csv file to your local machine. 
Enclosed will be a Google Poll. Please note that this software depends on the Google Poll format staying static, please do not make changes to the poll. You have "editing" privlages on the poll so that you may be able to download the CSV file.

https://docs.google.com/forms/d/e/1FAIpQLSdBOL2BnhtfO0yrURINfBG4C0iZw634bc6RT6PMCQkvh1o5bQ/viewform?usp=sf_link
 
It is important that you:
--save the csv file in the import folder
--name the file "userdata.csv"

You can now run the TeamSort simulation. From the repo home there is a file called TeamSort.sh. Run the following command:

sh TeamSort.sh

You will be prompted for how many teams you would like your class divided into.

The resulting optomized teams will be displayed for you in the command prompt upon completion of the sort.



=======

