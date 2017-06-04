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
User Guide + Program Configuration:

In command prompt (Terminal for Mac) enter "git clone https://github.com/astraub2/CIS422DEVEL.git"

Change directory to the CIS422DEVEL folder.

Enter "git pull origin web_app"

Copy and rename the file "CONFIG.base.py" to "CONFIG.py"

Enter valid login information for database access (your login information)

Install the necessary modules (if needed):
pip install -r requirements.txt

Install the necessary modules into the virtual environment:
make env

Install the virtual environment and run program:
make run

Once command prompt displays the message "* Running on http://0.0.0.0:9001/ (Press CTRL+C to quit)"

Open your web browser and go to the url: http://0.0.0.0:9001/

Sign up/Login with your credentials. 

Click on the Manage button in the top right corner. 

There will be an option to "Select all members". Click the checkbox next to this and hit the generate button. 

Go back to Command prompt and enter the number of groups you would the class to be divided into. 

Once this is done, the web app should display the different groups by email. 

Uninstall the program from the system:
make veryclean

---------------------------------------------------------------------
---------------------------------------------------------------------
FEATURES:

WebApp:
With our webapp, we have moved away from using an outside poll/survey to get data from students. Students will be logging on and then filling out the survey. This allowed us to be able to customize our survey more easily. 

We have also added the ability for the admin to decide which features they would like to prioritize. Based on what the admin chooses, the scoring system will be adjusted. 

Sorting Algorithm:
4 main criteria: scheduling, strengths, weaknesses, and teammate preference. 

The more well suited a team is for each other, the higher “score” they have. The default is the more available times to meet among students in a team, results in a higher score. (ie. If a teammate’s strengths match another teammate’s weaknesses, the score is higher.)
Finally, if a teammate is placed in a group with someone they preferred, the score of the team is higher. 

First, the program randomly assigns students to a team. Then the teams will be shuffled 1000 times with the intent of maximizing team scores to create higher compatibility. After maximizing, the algorithm will output what the new teams are. 

Currently the algorithm is set up to allow the admin to decide which criteria they would like to prioritize. However we do not have ability to do so from our webapp. This must be done from within the algorithm and there are instructions provided for that in the comments of the flask_main.py file. 

---------------------------------------------------------------------
---------------------------------------------------------------------
 
*******

If you would like to test TeamSort without generating data, good news!!! We have TestData. It can be ran from the command line using: make testdata

*******
