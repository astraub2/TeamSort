import flask

from flask import flash
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

import json
import logging
import base64

import random
import time
import pdb
import copy
import json

# Date Handling
import arrow
import datetime
from dateutil import tz

# Mongo Database
from pymongo import MongoClient
from bson import ObjectId

#########
#
# GLOBALS
#
#########


import CONFIG

app = flask.Flask(__name__)

print("Entering Setup")

try:
	dbclient = MongoClient(CONFIG.MONGO_URL)
	db = dbclient.classdata
	collection = db.accounts

except:
	print("Failure to open database. Is the Mongo server running? Correct Password?")
	sys.exit(1)

import uuid
app.secret_key = str(uuid.uuid4())

#######
#
# PAGES
#
#######

@app.route("/")
@app.route("/index")
def index():
	app.logger.debug("Main page entry")

	#Clears any saved user data upon returning to the splash page.
	clear_session()
	
	return render_template('splash.html')

@app.route("/signup")
def signup():
	app.logger.debug("Account Creation page entry")
	return render_template('signup.html')

@app.route("/avail")
def avail():
	app.logger.debug("Availability page entry")
	return render_template('avail.html')

@app.route("/exp")
def exp():
	app.logger.debug("Experience page entry")
	return render_template('exp.html')
	
@app.route("/login")
def login():
	Algorithm()

	app.logger.debug("Login page entry")
	return render_template('login.html')

@app.route("/dashboard")
def landing():
	app.logger.debug("Dashboard page entry")
	app.logger.debug("Getting accounts now")
	
	accountID = flask.session['user']
	account =  collection.find_one({"_id": ObjectId(accountID)})
	login = account['login']
	
	flask.session['first'] = login['first']
	flask.session['last'] = login['last']
	flask.session['email'] = login['email']
	flask.session['avail'] = account['avail']
	flask.session['accounts'] = get_accounts()
	
	return render_template('main.html')
	
@app.route("/user")
def user():
	app.logger.debug("Update account page entry")
	app.logger.debug("Getting account now")
	return render_template('usermenu.html')
	
@app.route("/manage")
def manage():
	app.logger.debug("Manage page entry")
	return render_template('manage.html')

@app.errorhandler(404)
def page_not_found(error):
	app.logger.debug("Page not found")
	return render_template('page_not_found.html', badurl=request.base_url, linkback=url_for("index")), 404

####################
#
# TEMPLATE FUNCTIONS
#
####################

@app.template_filter('humanize')
def humanize_arrow_date(date):
	"""
	Output should be "today", "yesterday", "in X days", etc.
	Arrow will try to humanize down to the minute, so we need to catch 'today'
	as a special case.
	"""

	try:
		then = arrow.get(date).to('local')
		now = arrow.utcnow().to('local')
		if then.date() == now.date():
			human = "Today"
		else:
			human = then.humanize(now)
			if human == "in a day":
				human = "Tomorrow"
	except:
		human = date
	return human

@app.route("/_signup", methods=["POST"])
def create_account():
	"""
	Creates and inserts a new account into the database
	"""
	
	#Clear session variables on action
	clear_session()
	
	print("Getting account information...")
	first = request.form.get('RegisterFirstNameInput', '', type=str)
	last = request.form.get('RegisterLastNameInput', '', type=str)
	s_id = request.form.get('RegisterIDInput', '', type=str)
	email = request.form.get('RegisterEmailInput', '', type=str)
	pwd = request.form.get('RegisterPasswordInput', '', type=str)
	confirm = request.form.get('LoginRepeatInput', '', type=str)
	
	#Clears any excess whitespace
	first.strip()
	last.strip()
	s_id.strip()
	email.strip()

	print("Testing account information...")
	if signup_errors(first, last, s_id, email, pwd, confirm) == True:
		return redirect("/signup")
	
	print("Account check initiated...")
	if collection.find_one({"user": email}) is not None:
		flash("Account already created!")
		return redirect("/login")

	print("Encrypting password...")
	pwd = base64.b64encode(pwd.encode('utf-8'))
	flask.session['pwd'] = pwd

	flask.session['login'] = {'first': flask.session['first'], 'last': flask.session['last']
							, 'id': flask.session['id'], 'email': flask.session['email']
							, 'pwd': flask.session['pwd']}

	#Clear session variables from preloading
	clear_session()

	return redirect("/avail")

@app.route("/_avail", methods=["POST"])
def init_avail():
	"""
	Updates new accounts with initial account availability and experience
	"""
	#Pulls data from table
	moAvail = request.form.getlist('mo')
	tuAvail = request.form.getlist('tu')
	weAvail = request.form.getlist('we')
	thAvail = request.form.getlist('th')
	frAvail = request.form.getlist('fr')

	workAvail = {'Monday': moAvail, 'Tuesday': tuAvail, 'Wednesday': weAvail, 'Thursday': thAvail, 'Friday': frAvail}
	
	flask.session['avail'] = workAvail
	
	return redirect("/exp")

@app.route("/_exp", methods=["POST"])
def init_exp():
	"""
	Updates new accounts with initial account availability and experience
	"""
	
	login = flask.session['login']
	avail = flask.session['avail']
	
	#Pull data from language data and appends the valid info into a tuple list
	#i.e. (Language, Score)
	langData = []
	
	if request.form.get('java'):
		langData.append(('java', request.form.get('java')))
	
	if request.form.get('c'):
		langData.append(('c', request.form.get('c')))

	if request.form.get('python'):
		langData.append(('python', request.form.get('python')))
	
	if request.form.get('swift'):
		langData.append(('swift', request.form.get('swift')))
	
	if request.form.get('php'):
		langData.append(('php', request.form.get('php')))

	if request.form.get('javascript'):
		langData.append(('javascript', request.form.get('javascript')))

	if request.form.get('specified', '', type=str):
		otherTuple =(request.form.get('specified', '', type=str), request.form.get('other'))
		langData.append(otherTuple)
				
	#Pull data from course data and appends the valid info into a tuple list
	#i.e. (Course, [weak/str])
				
	courseData = []
				
	if request.form.get('313'):
		courseData.append(('313', request.form.get('313')))
	
	if request.form.get('314'):
		courseData.append(('314', request.form.get('314')))

	if request.form.get('315'):
		courseData.append(('315', request.form.get('315')))
	
	if request.form.get('322'):
		courseData.append(('322', request.form.get('322')))
						
	if request.form.get('330'):
		courseData.append(('330', request.form.get('330')))
						
	if request.form.get('415'):
		courseData.append(('415', request.form.get('415')))
						
	if request.form.get('425'):
		courseData.append(('425', request.form.get('425')))

	#Pull teammate preference
	if request.form.get('TeamPrefInput', '', type=str):
		exp = {'pro': langData, 'per': courseData, 'pref': request.form.get('TeamPrefInput', '', type=str)}
	else:
		exp = {'pro': langData, 'per': courseData, 'pref': ''}

	insert_account(login, avail, exp)

	#Clear session variables before redirect
	flask.session['login'] = None
	flask.session['avail'] = None
	flask.session['exp'] = None

	return redirect("/login")

@app.route("/_login", methods=["POST"])
def login_user():
	"""
	Logs user in
	"""
	
	input_email = request.form.get('LoginEmailInput')
	input_pwd = request.form.get('LoginPasswordInput')
	
	#Strips any excess whitespace and then attempts to find a user
	account = collection.find_one({"user": input_email.strip()})
	print(account)
	if account is None:
		flash("Account not found!")
		return redirect("/login")

	login = account["login"]
	pwd = base64.b64decode(login["pwd"]).decode("utf-8")

	if input_pwd == pwd:
		#Sets the login session for the user
		flask.session['user'] =  str(account['_id'])
		
		return redirect("/dashboard")
	else:
		flash("Invalid credentials.")

	if not input_pwd:
		flash("No password entered.")
	
	return redirect("/login")

@app.route("/_manage")
def manage_accounts():
	"""
	Manage accounts by accountID
	"""

	print("Getting selected account ids and action...")
	selectedAccounts = request.form.getlist('selected')
	actionToPerform = request.form.get('action')
	
	if actionToPerform == "delete":
		print("Deleting accounts...")
		for accountID in selectedAccounts:
			account =  collection.find_one({"_id": ObjectId(accountID)})
			collection.remove(account)

	if actionToPerform == "generate":
		print("Generating data to be sorted")
		
		groupSize = request.form.get('GroupSizeInput')
		groupSizeRange = request.form.get('GroupSizeRangeInput')
		
		accountData = []
		for accountID in selectedAccounts:
			account =  collection.find_one({"_id": ObjectId(accountID)})
			accountData.append(account)



	return redirect("/manage")
	
@app.route("/_update", methods=["POST"])
def update_user():
	"""
	Update user information
	"""
	accountID = flask.session['user']
	print(flask.session['first'])
	
	mon = request.form.get('mon', '', type=str)
	tue = request.form.get('tue', '', type=str)
	wed = request.form.get('wed', '', type=str)
	thu = request.form.get('thu', '', type=str)
	fri = request.form.get('fri', '', type=str)
	sat = request.form.get('sat', '', type=str)
	sun = request.form.get('sun', '', type=str)
	avail = mon + tue + wed + thu + fri + sat + sun
	
	first = request.form.get('first', '', type=str)
	last = request.form.get('last', '', type=str)
	major = request.form.get('major', '', type=str)
	email = request.form.get('email', '', type=str)
	phone = request.form.get('phone', '', type=str)
	quote = request.form.get('quote', '', type=str)
	
	if not avail:
		avail = flask.session['avail']		
	if not first:
		first = flask.session['first']
	if not last:
		last = flask.session['last']
	if not major:
		major = flask.session['major']
	if not email:
		email = flask.session['email']
	if not phone:
		phone = flask.session['phone']
	if not quote:
		quote = flask.session['quote']
		
	collection.update({"_id": ObjectId(accountID)},{'$set':{'avail':avail,'first':first,'last':last,'major':major,'email':email,'phone':phone,'quote':quote}})
	flash("Your user information has been updated!")
	return redirect("/dashboard")
	
	
######################
#
# SUPPORTING FUNCTIONS
#
######################

def get_accounts():
	"""
	Returns all accounts in the database, in a form that
	can be inserted directly in the 'session' object.
	"""
	
	print("get_accounts() started.")
	accounts = []
	for account in collection.find({"type" : "account"}):
		account['date'] = arrow.get(account['date']).isoformat()
		account['_id'] = str(account['_id'])
		accounts.append(account)

	accounts.sort(key=lambda a: a["date"])
	return accounts

def insert_account(login, avail, exp):
	"""
	Inserts an new account into the database with minimum user info
	"""
	date = arrow.utcnow().format('MM/DD/YYYY')
	dt = arrow.get(date, 'MM/DD/YYYY').replace(tzinfo='local')
	iso_dt = dt.isoformat()
	
	print("Compiling new account from data")
	account = {
		"type" :  "account",
			"date"	: iso_dt,
			"role"	: "admin",
			"user"	: login["email"],
			"login" : login,
			"avail" : avail,
			"exp"	: exp
	}

	collection.insert(account)
	print("Account has been inserted into the database.")
	flash("Account created! You may now login.")
	
	return

def clear_session():
	"""
	Calling this function will clear all of the session variables used for login redirect
	"""

	flask.session['first'] = None
	flask.session['last'] = None
	flask.session['id'] = None
	flask.session['email'] = None
	flask.session['pwd'] = None

	return
TEST_DATA = False

def generateUserData():
	
	accounts=get_accounts()
	#print(accounts)
	experiencearray=[]
	bexperiencearray=[]
	emailarray=[]
	availarray=[]
	for i in accounts:
		email=i['user']
		availability=i['avail']

		experience=i['exp']['pro']
		
		myexperience=[]
		
		bmyexperience=[]
		##########
		#Grab usernames
		###########
		emailarray.append(email)

		#############
		#Grab experiences
		############
		for i in experience:
			lan=i[0]
			lev=i[1]
			if int(lev)>3:
				myexperience.append(lan)
				#print(lan)
			else:
				bmyexperience.append(lan)

		experiencearray.append(myexperience)
		bexperiencearray.append(bmyexperience)
		

		#############
		#Grab avaibility
		############
		#print(availability)
		DAYS=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
		count=0
		myavail=[]
		for i in availability:
			#print(i)
			if i in DAYS:
				timesonday=availability[DAYS[count]]
				#print(availability[DAYS[count]])

				for j in timesonday:
					#print(i+" " +j)
					myavail.append(i+" " +j)
			count+=1
		availarray.append(myavail)
		# print ("\n\n")
		# print(i['user'])
		# print(i['exp']['pro'])
		# print(i['avail'])
	# print(emailarray)
	# print(experiencearray)
	# print(bexperiencearray)
	# print(availarray)
	users=[]
	count=0
	for i in emailarray:
		users.append([emailarray[count], availarray[count], experiencearray[count], bexperiencearray[count]])
		count+=1
	#print(emailarray)
	#print(users)

	data={
	"schedule_list" : ['Wednesday 8', 'Wednesday 8:30', 'Wednesday 9', 'Wednesday 9:30', 'Wednesday 10', 'Wednesday 10:30', 'Wednesday 11', 'Wednesday 11:30', 'Wednesday 12', 'Wednesday 12:30', 'Wednesday 13', 'Wednesday 13:30', 'Wednesday 14', 'Wednesday 14:30', 'Wednesday 15', 'Wednesday 15:30', 'Wednesday 16', 'Wednesday 16:30', 'Wednesday 17', 'Wednesday 17:30', 'Wednesday 18', 'Wednesday 18:30', 'Tuesday 8', 'Tuesday 8:30', 'Tuesday 9', 'Tuesday 9:30', 'Tuesday 10', 'Tuesday 10:30', 'Tuesday 11', 'Tuesday 11:30', 'Tuesday 12', 'Tuesday 12:30', 'Tuesday 13', 'Tuesday 13:30', 'Tuesday 14', 'Tuesday 14:30', 'Tuesday 15', 'Tuesday 15:30', 'Tuesday 16', 'Tuesday 16:30', 'Tuesday 17', 'Tuesday 17:30', 'Tuesday 18', 'Tuesday 18:30', 'Friday 8', 'Friday 8:30', 'Friday 9', 'Friday 9:30', 'Friday 10', 'Friday 10:30', 'Friday 11', 'Friday 11:30', 'Friday 12', 'Friday 12:30', 'Friday 13', 'Friday 13:30', 'Friday 14', 'Friday 14:30', 'Friday 15', 'Friday 15:30', 'Friday 16', 'Friday 16:30', 'Friday 17', 'Friday 17:30', 'Friday 18', 'Friday 18:30', 'Monday 8', 'Monday 8:30', 'Monday 9', 'Monday 9:30', 'Monday 10', 'Monday 10:30', 'Monday 11', 'Monday 11:30', 'Monday 12', 'Monday 12:30', 'Monday 13', 'Monday 13:30', 'Monday 14', 'Monday 14:30', 'Monday 15', 'Monday 15:30', 'Monday 16', 'Monday 16:30', 'Monday 17', 'Monday 17:30', 'Monday 18', 'Monday 18:30', 'Thursday 8', 'Thursday 8:30', 'Thursday 9', 'Thursday 9:30', 'Thursday 10', 'Thursday 10:30', 'Thursday 11', 'Thursday 11:30', 'Thursday 12', 'Thursday 12:30', 'Thursday 13', 'Thursday 13:30', 'Thursday 14', 'Thursday 14:30', 'Thursday 15', 'Thursday 15:30', 'Thursday 16', 'Thursday 16:30', 'Thursday 17', 'Thursday 17:30', 'Thursday 18', 'Thursday 18:30'],
	"skill_list" :['java', 'python', 'swift', 'php', 'c', 'javascript'],
	"users" : users, 
	"current_index" : 0,
	"priority" : [1,1,1]
	}

	#print (accounts)
	return data

def regenerateUserData(newemailarray):
	
	accounts=get_accounts()
	print(accounts)
	print('HIIIIIIIIIIIi')
	experiencearray=[]
	bexperiencearray=[]
	emailarray=[]
	availarray=[]
	for i in accounts:
		email=i['user']
		if email in newemailarray:
			availability=i['avail']

			experience=i['exp']['pro']
			
			myexperience=[]
			
			bmyexperience=[]
			##########
			#Grab usernames
			###########
			emailarray.append(email)

			#############
			#Grab experiences
			############
			for i in experience:
				lan=i[0]
				lev=i[1]
				if int(lev)>3:
					myexperience.append(lan)
					#print(lan)
				else:
					bmyexperience.append(lan)

			experiencearray.append(myexperience)
			bexperiencearray.append(bmyexperience)
			

			#############
			#Grab avaibility
			############
			#print(availability)
			DAYS=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
			count=0
			myavail=[]
			for i in availability:
				#print(i)
				if i in DAYS:
					timesonday=availability[DAYS[count]]
					#print(availability[DAYS[count]])

					for j in timesonday:
						#print(i+" " +j)
						myavail.append(i+" " +j)
				count+=1
			availarray.append(myavail)
			#############
			#Grab prefered teamate
			############

		# print ("\n\n")
		# print(i['user'])
		# print(i['exp']['pro'])
		# print(i['avail'])
	# print(emailarray)
	# print(experiencearray)
	# print(bexperiencearray)
	# print(availarray)
	users=[]
	count=0
	for i in emailarray:
		users.append([emailarray[count], availarray[count], experiencearray[count], bexperiencearray[count]])
	print(emailarray)

	data={
	"schedule_list" : ['Wednesday 8', 'Wednesday 8:30', 'Wednesday 9', 'Wednesday 9:30', 'Wednesday 10', 'Wednesday 10:30', 'Wednesday 11', 'Wednesday 11:30', 'Wednesday 12', 'Wednesday 12:30', 'Wednesday 13', 'Wednesday 13:30', 'Wednesday 14', 'Wednesday 14:30', 'Wednesday 15', 'Wednesday 15:30', 'Wednesday 16', 'Wednesday 16:30', 'Wednesday 17', 'Wednesday 17:30', 'Wednesday 18', 'Wednesday 18:30', 'Tuesday 8', 'Tuesday 8:30', 'Tuesday 9', 'Tuesday 9:30', 'Tuesday 10', 'Tuesday 10:30', 'Tuesday 11', 'Tuesday 11:30', 'Tuesday 12', 'Tuesday 12:30', 'Tuesday 13', 'Tuesday 13:30', 'Tuesday 14', 'Tuesday 14:30', 'Tuesday 15', 'Tuesday 15:30', 'Tuesday 16', 'Tuesday 16:30', 'Tuesday 17', 'Tuesday 17:30', 'Tuesday 18', 'Tuesday 18:30', 'Friday 8', 'Friday 8:30', 'Friday 9', 'Friday 9:30', 'Friday 10', 'Friday 10:30', 'Friday 11', 'Friday 11:30', 'Friday 12', 'Friday 12:30', 'Friday 13', 'Friday 13:30', 'Friday 14', 'Friday 14:30', 'Friday 15', 'Friday 15:30', 'Friday 16', 'Friday 16:30', 'Friday 17', 'Friday 17:30', 'Friday 18', 'Friday 18:30', 'Monday 8', 'Monday 8:30', 'Monday 9', 'Monday 9:30', 'Monday 10', 'Monday 10:30', 'Monday 11', 'Monday 11:30', 'Monday 12', 'Monday 12:30', 'Monday 13', 'Monday 13:30', 'Monday 14', 'Monday 14:30', 'Monday 15', 'Monday 15:30', 'Monday 16', 'Monday 16:30', 'Monday 17', 'Monday 17:30', 'Monday 18', 'Monday 18:30', 'Thursday 8', 'Thursday 8:30', 'Thursday 9', 'Thursday 9:30', 'Thursday 10', 'Thursday 10:30', 'Thursday 11', 'Thursday 11:30', 'Thursday 12', 'Thursday 12:30', 'Thursday 13', 'Thursday 13:30', 'Thursday 14', 'Thursday 14:30', 'Thursday 15', 'Thursday 15:30', 'Thursday 16', 'Thursday 16:30', 'Thursday 17', 'Thursday 17:30', 'Thursday 18', 'Thursday 18:30'],
	"skill_list" :['java', 'python', 'swift', 'php', 'c', 'javascript'],
	"users" : users, 
	"current_index" : 0,
	"priority" : [1,1,1]}

	#print (accounts)
	return data



class UserData:
	def __init__(self):
		if TEST_DATA:
			with open("testdata.txt") as test_file:
				self.db = json.load(test_file)
		else:
			self.db = generateUserData()

	def get_user_count(self):
		return len(self.db["users"])

	def get_group_count(self):
		# Read group count from database
		return self.db["group_count"] 

	def set_group_count(self, groupcount):
		self.db["group_count"] = groupcount

	def get_next_user(self):
		next_user = None
		if self.db["current_index"] < len(self.db["users"]):
			next_user = self.db["users"][self.db["current_index"]]
			self.db["current_index"] += 1
		return next_user

	def reset_user_list(self):
		self.db["current_index"] = 0
		random.shuffle(self.db["users"]);
		
	def get_schedule_list(self):
		return self.db["schedule_list"]

	def get_skill_list(self):
		return self.db["skill_list"]

	# There are 3 things the admin can prioritize when running the algorithm: schedule, strength/weakness, and teammmate preference
	def set_priorities(self, pri):
		"""
		pri should be an array which at null is [1,1,1]
		Index 0 corresponds to scheduling, index 1 corresponds to strength/weakness and index 2 corresponds to teammate preference
		If you want to select a feature to prioritize, increase the index of that feature by 1
		For example, if I wanted to prioritize scheduling, pri = [2,1,1]
		If I wanted to prioritize strengths/weakness, pri = [1,2,1]
		If I wanted to prioritize teammate preference, pri = [1,1,2]
		If user has no priority, simply do not call this function in main()
		"""
		self.db["priority"] = pri

	def get_priorities(self):
		return self.db["priority"]

# User indices
U_NDX_NAME = 0
U_NDX_SCHD = 1
U_NDX_STRN = 2
U_NDX_WEAK = 3
U_NDX_PREF = 4

# Group indices
G_NDX_SCORE = 0
G_NDX_USERS = 1

# Points
PRIORITY_SCHED = 0
PRIORITY_SKILL = 1
PRIORITY_PREF = 2

class Groups:
	def __init__(self, groupcount):
		self.groupcount = groupcount
		# Groups will be built with data read from database.
		# Group data strucutures are modeled as follows
		'''
		schedules = ["Monday 8 AM to 10 AM", "Monday 10 AM to 12 PM", .......]
		skills = ["Java", "C", "C++", "Python", "PHP", "JavaScript", "Web Server", "shell"]
		group[i] = [
			computed_group_weight, 
			{
				"usr_name0" : ["usr_name0", [list of schedules], [list of strengths], [list of weaknesses], [list of preferred_teammate]],
				"usr_name1" : ["usr_name1", [list of schedules], [list of strengths], [list of weaknesses], [list of preferred_teammate]],
				"usr_name2" : ["usr_name2", [list of schedules], [list of strengths], [list of weaknesses], [list of preferred_teammate]],
				"usr_name3" : ["usr_name3", [list of schedules], [list of strengths], [list of weaknesses], [list of preferred_teammate]],
			},
		]

		'''

		# Initialize the database.
		db = UserData()

		self.priority = db.get_priorities()

		# Fetch the number of users and number of groups
		N = db.get_user_count()
		# G = db.get_group_count()
		G = self.groupcount
		db.set_group_count(G)

		# Need to add users randomly to groups.  So let's randomize the sequence of groups
		group_index_list = list(range(G))
		random.shuffle(group_index_list)

		# Now create groups with users
		group_index = 0
		self.groups = []
		for i in range(G):
			self.groups.append([0, {}])
		db.reset_user_list()
		while True:
			user_rec = db.get_next_user()
			if user_rec == None:
				break

			g = self.groups[group_index_list[group_index]]
			g[G_NDX_USERS][user_rec[U_NDX_NAME]] = user_rec

			group_index += 1
			if group_index >= G:
				group_index = 0

		# Now do the initial scoring of groups
		for i in range(G):
			self._compute_group_score(self.groups[i])

	def _compute_group_score(self, group):
		group[G_NDX_SCORE] = 0

		user_list = group[G_NDX_USERS].keys();
		for user in user_list:
			for other in user_list:
				if user == other:
					continue

				for i in group[G_NDX_USERS][user][U_NDX_SCHD]:
					if i in group[G_NDX_USERS][other][U_NDX_SCHD]:
						group[G_NDX_SCORE] += self.priority[PRIORITY_SCHED]

				for i in group[G_NDX_USERS][user][U_NDX_WEAK]:
					if i in group[G_NDX_USERS][other][U_NDX_STRN]:
						group[G_NDX_SCORE] += self.priority[PRIORITY_SKILL]

				# for i in group[G_NDX_USERS][user][U_NDX_PREF]:
				# 	if i == group[G_NDX_USERS][other][U_NDX_NAME]:
				# 		group[G_NDX_SCORE] += self.priority[PRIORITY_PREF]

	def get_size(self):
		return len(self.groups)

	def get_random_group(self):
		return random.choice(self.groups)

	def extract_random_user_from_group(self, group):
		r_user_name = random.choice(list(group[G_NDX_USERS].keys()))
		user_rec = copy.deepcopy(group[G_NDX_USERS][r_user_name])

		del group[G_NDX_USERS][r_user_name]
		self._compute_group_score(group)
		return user_rec

	def add_user_to_group(self, group, user_record):
		group[G_NDX_USERS][user_record[U_NDX_NAME]] = user_record
		self._compute_group_score(group)

	def remove_user_from_group(self, group, user_name):
		user_rec = group[G_NDX_USERS][user_name]

		del group[G_NDX_USERS][user_name]
		self._compute_group_score(group)

	def print_groups_scores(self, group_index):
		print(self.groups[group_index][G_NDX_SCORE], end = "  ")
		print(list(self.groups[group_index][G_NDX_USERS].keys()))

	def get_group_score(self, group):
		return group[G_NDX_SCORE]

	def get_group(self, index):
		if index < self.get_size():
			return self.groups[index]
		else:
			return None 

	def run_simulation(self, arr_group):
		for i in range(5000):
			rg1 = self.get_group(random.choice(arr_group))
			rg2 = self.get_group(random.choice(arr_group))

			if rg1 == rg2: continue
			rg1_score = self.get_group_score(rg1)
			rg2_score = self.get_group_score(rg2)

			user1 = self.extract_random_user_from_group(rg1)
			user2 = self.extract_random_user_from_group(rg2)

			self.add_user_to_group(rg1, user2)
			self.add_user_to_group(rg2, user1)

			new_rg1_score = self.get_group_score(rg1)
			new_rg2_score = self.get_group_score(rg2)

			if new_rg1_score < rg1_score or new_rg2_score < rg2_score or new_rg1_score < new_rg2_score:
				self.remove_user_from_group(rg1, user2[U_NDX_NAME])
				self.add_user_to_group(rg1, user1)
				self.remove_user_from_group(rg2, user1[U_NDX_NAME])
				self.add_user_to_group(rg2, user2)


def Algorithm():
	#pdb.set_trace()

	random.seed(int(time.time()))
	n = int(input("Enter the number of groups: "))
	groups = Groups(n)
	group_size = groups.get_size()

	print("==== Groups before simulation ====")
	for i in range(group_size):
		groups.print_groups_scores(i)

	print("Working...")
	arr_group = range(group_size)
	groups.run_simulation(arr_group)

	print("==== Groups after simulation ====")
	for i in range(group_size):
		groups.print_groups_scores(i)

	arr_group = [0,1,2]
	groups.run_simulation(arr_group)
	print("==== Groups after sub-group simulation ====")
	for i in range(group_size):
		groups.print_groups_scores(i)

	arr_priority = [1,1,2]
	#groups.set_priority(arr_priority)
	groups.run_simulation(arr_group)

	print("==== Groups after changing priority (sched to teammate) ====")
	for i in range(group_size):
		groups.print_groups_scores(i)




def signup_errors(first, last, s_id, email, pwd, confirm):
	"""
	Tests the signup information given for input errors
	"""
	error = False
	
	#First Name Input Error Handling
	if not first:
		flash("No first name given.")
		error = True
	else:
		flask.session['first'] = first
	
	#Last Name Input Error Handling
	if not last:
		flash("No last name given.")
		error = True
	else:
		flask.session['last'] = last

	#Student ID Input Error Handling
	if not s_id:
		flash("No ID given.")
		error = True

	else:
		if s_id.startswith("95") == False:
			flash("ID must begin with 95.")
			error = True

		if len(s_id) != 9:
			flash("ID must be 9 digits.")
			error = True

		else:
			flask.session['id'] = s_id

	#E-mail Input Error Handling
	if not email:
		flash("No email given.")
		error = True
	else:
		flask.session['email'] = email

	#Password Input Error Handling
	if not pwd:
		flash("No password given.")
		error = True

	if pwd != confirm:
		flash("The passwords you entered did not match.")
		error = True

	return error

if __name__ == "__main__":
	app.debug=CONFIG.DEBUG
	app.logger.setLevel(logging.DEBUG)

	if CONFIG.DEBUG:
		# Reachable only from the same computer
		app.run(port=CONFIG.PORT)
	else:
		# Reachable from anywhere
		app.run(port=CONFIG.PORT,host="0.0.0.0")
