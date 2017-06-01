import flask

from flask import flash
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

import json
import logging
import base64

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
