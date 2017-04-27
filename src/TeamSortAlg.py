#!/usr/bin/env python3

# Vinitha Gadiraju
# Algorithm

import random
import time
import pprint
import pdb
import copy
import psycopg2


# Using static data.  Set this to false to use data from database
TEST_DATA = False

test_data = {
	"group_count" : 5,
	"schedule_list" : ["Monday 8 AM to 10 AM", "Monday 10 AM to 12 PM", "Monday 12 PM to 2 PM", 
		"Monday 2 PM to 4 PM", "Monday 4 PM to 6 PM", "Monday 6 PM to 8 PM"],
	"skill_list" : ["Java", "C", "C++", "Python", "PHP", "JavaScript", "Web Server", "shell"],
	"users" : [
		["tom", [0,1,2], ["Java", "C", "C++"], ["Python", "PHP"], ["will", "sue"]],
		["will", [1,3,5], ["JavaScript", "Web Server"], ["C", "C++"], ["bill", "kevin", "geeta"]],
		["sue", [4,5,1], ["JavaScript", "Web Server"], ["Java", "C", "C++"], ["vinitha", "tejal"]],
		["kevin", [0,3,5], ["Web Server", "shell"], ["Python", "PHP", "JavaScript"], ["manju", "roopa"]],
		["vinitha", [4,3,1], ["C", "C++"], ["PHP", "JavaScript", "Web Server"], ["nivitha", "vidya"]],
		["tejal", [0,3,6], ["JavaScript", "Web Server"], ["Java", "C", "C++", "Python"], ["vinay", "abhi"]],
		["roopa", [1,3,7], ["Python", "PHP", "JavaScript"], ["Java", "C", "C++"], ["vinay", "roger"]],
		["nivitha", [1,2,3], ["Java", "C", "C++"], ["Python", "PHP", "JavaScript"], ["vinay", "abhi", "geeta"]],
		["vidya", [4,2,3], ["Python", "PHP", "JavaScript"], ["C", "C++"], ["rishika", "avi"]],
		["vinay", [6,5,4], ["Java"], ["C++"], ["todd", "bill"]],
		["abhi", [4,3,1], ["JavaScript", "Web Server", "shell"], ["C", "C++"], ["tom", "avi"]],
		["manju", [1,2,5], ["C", "C++"], ["JavaScript", "shell"], ["vidya", "abhi"]],
		["todd", [4,6,3], ["Python", "PHP", "JavaScript"], ["C", "C++"], ["vinitha", "nivitha"]],
		["bill", [3,2,4], ["PHP", "shell"], ["C", "C++"], ["tejal", "manju", "abhi"]],
		["perd", [5,0,1,6,4], ["Java"], ["C", "C++", "shell"], ["roopa", "vinitha"]],
		["geeta", [1,5,6,0], ["Python"], ["Java", "C", "C++", "PHP", "JavaScript", "Web Server", "shell"], ["perd", "nivitha"]],
		["avi", [0,3,2,1], ["Python", "PHP", "JavaScript"], ["C", "C++"], ["rishika", "roopa", "bill"]],
		["rishika", [2,3,4,1], ["Java", "C", "C++", "Python", "PHP", "JavaScript"], ["Web Server", "shell"], ["bill", "todd", "roger"]],
		["roger", [3,4,1], ["Java", "C"], ["C++"], ["subbu", "manju", "willl"]],
		["subbu", [6,2,4], ["Python", "PHP", "JavaScript", "Web Server", "shell"], ["Java", "C", "C++"], ["will", "sue", "perd"]]
	],
	"current_index" : 0
}

def getnames():
	conn = psycopg2.connect(dbname='teamsort')
	cur = conn.cursor()
	cur.execute('SELECT username FROM users;')
	#Lets grab all of the usernames for the database:
	usernames=[]

	try:
	    result = cur.fetchall()
	except ProgrammingError:
	    result = None
	if result == None:
	    print("nothing")
	else:
	    for i in result:
	        usernames.append(i[0])
	#print (usernames)
	return usernames
def gettimes():
	conn = psycopg2.connect(dbname='teamsort')
	cur = conn.cursor()
	cur.execute('SELECT * FROM times;')
	#Lets grab all of the usernames for the database:
	times=[]

	try:
	    result = cur.fetchall()
	except ProgrammingError:
	    result = None
	if result == None:
	    print("nothing")
	else:
		theres=[]
		res=[]
		for i in result:
			for l in i:
				if l != None:
					try:
						l = int(l)
						if l<100:
							res.append(l)
					except ValueError:
						continue
					
			theres.append(res)
			res=[]
	#print(theres)
	return theres

def getstrengths():
	wordlan=['JAVA', 'CPP', 'SQL', 'HTML', 'PHP', 'Javascript', 'Bash', 'Git', 'Mongo', 'WSS', 'GIS', 'Python', 'PMO']
	conn = psycopg2.connect(dbname='teamsort')
	cur = conn.cursor()
	cur.execute('SELECT * FROM languages;')
	try:
	    result = cur.fetchall()
	except ProgrammingError:
	    result = None
	if result == None:
	    print("nothing")
	else:
		strengths=[]
		weaknesses=[]
		allstreng=[]
		allweak=[]
		for i in result:
			count=0
			for l in i:
				#print(l)
				if l != None:
					if isinstance(l, str):
						pass
					else:
						if l<100:
							strengths.append(wordlan[l])
							count=count+1
						else:
							weaknesses.append(wordlan[count])
							count=count+1

			allstreng.append(strengths)
			allweak.append(weaknesses)
			weaknesses=[]
			strengths=[]
	#print(allstreng)
	#print(allweak)
	return allstreng, allweak
def getpreferance():
	conn = psycopg2.connect(dbname='teamsort')
	cur = conn.cursor()
	cur.execute('SELECT * FROM users;')
	pref = []
	try:
	    result = cur.fetchall()
	except ProgrammingError:
	    result = None
	if result == None:
	    print("nothing")
	else:
		for i in result:
			pref.append([i[3]])

		#print(pref)

	return pref

def generateUserData(groupcount):
	usernames=getnames()
	times=gettimes()
	allstrengths, allweaknesses=getstrengths()
	pref=getpreferance()
	userdata=[]
	i=0
	for j in usernames:
		buildinstance=[]
		buildinstance.append(usernames[i])
		buildinstance.append(times[i])
		buildinstance.append(allstrengths[i])
		buildinstance.append(allweaknesses[i])
		buildinstance.append(pref[i])
		userdata.append(buildinstance)
		i+=1
	data={"group_count" : groupcount,
	"schedule_list" : ["Monday 8 AM to 10 AM", "Monday 10 AM to 12 PM", "Monday 12PM to 2 PM", "Monday 2 PM to 4 PM", "Monday 4 PM to 6 PM",
                        "Tuesday 8 AM to 10 AM", "Tuesday 10 AM to 12 PM", "Tuesday 12 PM to 2 PM", "Tuesday 2 PM to 4 PM", "Tuesday 4 PM to 6 PM",
                        "Wednesday 8 AM to 10 AM", "Wednesday 10 AM to 12 PM", "Wednesday 12 PM to 2 PM", "Wednesday 2 PM to 4 PM", "Wednesday 4 PM to 6 PM",
                        "Thursday 8 AM to 10 AM", "Thursday 10 AM to 12 PM", "Thursday 12 PM to 2 PM", "Thursday 2 PM to 4 PM", "Thursday 4 PM to 6 PM",
                        "Friday 8 AM to 10 AM", "Friday 10 AM to 12 PM", "Friday 12 PM to 2 PM", "Friday 2 PM to 4 PM", "Friday 4 PM to 6 PM",
                        "Saturday 8 AM to 10 AM", "Saturday 10 AM to 12 PM", "Saturday 12 PM to 2 PM", "Saturday 2 PM to 4 PM", "Saturday 4 PM to 6 PM",
                        "Sunday 8 AM to 10 AM", "Sunday 10 AM to 12 PM", "Sunday 12 PM to 2 PM", "Sunday 2 PM to 4 PM", "Sunday 4 PM to 6 PM"],
	"skill_list" :['JAVA', 'CPP', 'SQL', 'HTML', 'PHP', 'Javascript', 'Bash', 'Git', 'Mongo', 'WSS', 'GIS', 'Python', 'PMO'],
	"users" : userdata}
	#print(data)
	return data


pp = pprint.PrettyPrinter(indent=4)

class UserData:
	def __init__(self):
		if TEST_DATA:
			self.db = test_data
		else:
			self.db = generateUserData(5)

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

# User indices
U_NDX_NAME = 0
U_NDX_SCHD = 1
U_NDX_STRN = 2
U_NDX_WEAK = 3
U_NDX_TEAM = 4

# Group indices
G_NDX_SCORE = 0
G_NDX_USERS = 1

# Points
MATCH_POINTS_INCREMENT = 1

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
						group[G_NDX_SCORE] += MATCH_POINTS_INCREMENT

				for i in group[G_NDX_USERS][user][U_NDX_WEAK]:
					if i in group[G_NDX_USERS][other][U_NDX_STRN]:
						group[G_NDX_SCORE] += MATCH_POINTS_INCREMENT

				for i in group[G_NDX_USERS][user][U_NDX_TEAM]:
					if i == group[G_NDX_USERS][other][U_NDX_NAME]:
						group[G_NDX_SCORE] += MATCH_POINTS_INCREMENT


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

	def print_scores(self, group_index):
		print(self.groups[group_index][G_NDX_SCORE], end = "  ")
		print(list(self.groups[group_index][G_NDX_USERS].keys()))

	def get_group_score(self, group):
		return group[G_NDX_SCORE]


def main():
	#pdb.set_trace()
	random.seed(int(time.time()))
	n = int(input("Enter the number of groups: "))
	groups = Groups(n)
	group_size = groups.get_size()

	print("==== Groups before simulation ====")
	for i in range(group_size):
		groups.print_scores(i)

	print("Working...")
	for i in range(5000):
		rg1 = groups.get_random_group()
		rg2 = groups.get_random_group()

		if rg1 == rg2: continue

		user1 = groups.extract_random_user_from_group(rg1)
		user2 = groups.extract_random_user_from_group(rg2)

		groups.add_user_to_group(rg1, user2)
		groups.add_user_to_group(rg2, user1)

		if groups.get_group_score(rg1) < groups.get_group_score(rg2):
			groups.remove_user_from_group(rg1, user2[U_NDX_NAME])
			groups.add_user_to_group(rg1, user1)
			groups.remove_user_from_group(rg2, user1[U_NDX_NAME])
			groups.add_user_to_group(rg2, user2)

	print("==== Groups after simulation ====")
	for i in range(group_size):
		groups.print_scores(i)

if __name__ == '__main__':
	main()
