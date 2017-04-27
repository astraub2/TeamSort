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
tkinter
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
You must have tkinter successfully installed.

To install go to:
http://www.tkdocs.com/tutorial/install.html 

Follow directions for your system.

Do the same steps to install psycopg2 on your machine
---------------------------------------------------------------------
---------------------------------------------------------------------
FEATURES:

Database:
Having a database in the background leads to higher expansibility for
future projects and is better for data tracking.

Sorting Algorithm:
** vinitha's little blurb **

GUI Interface:
We decided to be able to read in the user's input on how big/small they
wanted their group size to be.
We also wanted the user to be able to specify a CSV file if they already
had the data instead of forcing them to manually input the data.
** if filename cannot be inputted, you must name file ______ **
---------------------------------------------------------------------
---------------------------------------------------------------------
User Guide:

Open the command line and clone this repository to your machine. You will need a basic understanding of git and command line interfaces to run this program. Verify that all required applications are in fact installed. 

Enclosed will be a Google Poll. Please note that this software depends on the Google Poll format staying static, please do not make changes to the poll. 
Once you recieve your data back from your students, use Google Poll to download the csv file to your local machine. 

It is important that you:
--save the csv file in the import folder
--name the file "userdata.csv"

You can now run the TeamSort simulation. From the repo home there is a file called TeamSort.sh. Run the following command:

sh TeamSort.sh

You will be prompted for how many teams you would like your class divided into.

The resulting optomized teams will be displayed for you in the command prompt upon completion of the sort.






=======

