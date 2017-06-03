Welcome to our CIS422 Development GitHub!

This repo is dedicated to a TeamSort project for sorting 
students into groups in future 422 classes.

Team Members:
Vinitha Gadiraju
Amber Straub
Anisha Aggarwal
Jared Smith

---------------------------------------------------------------------
---------------------------------------------------------------------
In order to run our TeamSort, you must have the following apps installed:
Python 3
---------------------------------------------------------------------
You must have Python 3 successfully installed.
To check if the correct version is installed: python3 -V in the command prompt. 

To install go to:
https://www.python.org/downloads/

Follow directions for your system. 
---------------------------------------------------------------------
You must have Homebrew successfully installed.

To install from command line:
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

Install the necessary modules (if needed):
brew arrow
brew flask
brew pymongo

Configure program:
Copy and rename CONFIG.base.py to CONFIG.py
Enter valid login information for database access (your login information)

Install the necessary modules (if needed):
pip install -r requirements.txt

Install the necessary modules into the virtual environment:
make install

Install the virtual environment and run program:
make run

Uninstall the program from the system:
make veryclean

---------------------------------------------------------------------
---------------------------------------------------------------------
FEATURES:

WebApp:
With our webapp, we have moved away from using an outside poll/survey to get data from students. Students will be logging on and then filling out the survey. This allowed us to be able to customize our survey more easily. 

We have also added the ability for the admin to decide which features they would like to priotitize. Based on what the admin chooses, the scoring system will be adjusted. 

Sorting Algorithm:
4 main criteria: scheduling, strengths, weaknesses, and teammate preference. 

The more well suited a team is for each other, the higher “score” they have. The default is the more available times to meet among students in a team, results in a higher score. (ie. If a teammate’s strengths match another teammate’s weaknesses, the score is higher.)
Finally, if a teammate is placed in a group with someone they preferred, the score of the team is higher. 

First, the program randomly assigns students to a team. Then the teams will be shuffled 1000 times with the intent of maximizing team scores to create higher compatibility. After maximizing, the algorithm will output what the new teams are. If the admin would like to regenerate the teams for any reason, they have the ability to do so. 

Currently the algorithm is set up to allow the admin to deicde which crition they would like to prioritize. However we do not have ability to do so from our webapp. This must be done from within the algorithm and there are instructions provided for that in the comments.

---------------------------------------------------------------------
---------------------------------------------------------------------
User Guide:

Provide the webapp link to all students. From the link, they will create an account and then fill out the survey. 

It should be noted that when inputting teammate preference, you must have both the first and last names spelled correctly in order for the algorithm to use that piece of information.

As an admin, you will have the ability to be able to decide which features you would like to priotitize. Once all the students have inputted data, you will press the "generate" button to generate the groups. They will then be displayed on the website. These results will be visible to the students as well (revealing no information about what information was filled out during the survey). 
 
It is important that you:
--save the csv file in the import folder
--name the file "userdata.csv"

*******
<<<<<<< HEAD
If you would like to test TeamSort without generating data, good news!!! We have TestData. It can be ran from the command line using: make testdata
=======

If you would like to test TeamSort without generating data, good news!!! We have created a fake set of data for you to test with called TestData. Turn on TestData and generate the data.
>>>>>>> dev

*******

You can now run the TeamSort simulation. From the repo home there is a file called TeamSort.sh. Run the following command:

sh TeamSort.sh

You will be prompted for how many teams you would like your class divided into.

The resulting optomized teams will be displayed for you in the command prompt upon completion of the sort.

=======

