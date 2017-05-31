#!/usr/bin/env python3

# Vinitha Gadiraju
# Algorithm

import random
import time
import pprint
import pdb
import copy
import psycopg2
import json

# Using static data.  Set this to false to use data from database
TEST_DATA = True

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
			with open("testdata.txt") as test_file:
				self.db = json.load(test_file)
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

	def get_priorities(self):
		return self.db["priority"]

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

				for i in group[G_NDX_USERS][user][U_NDX_TEAM]:
					if i == group[G_NDX_USERS][other][U_NDX_NAME]:
						group[G_NDX_SCORE] += self.priority[PRIORITY_PREF]


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

	def set_priority(self, arr_priority):
		self.priority = arr_priority

	def print_scores(self, group_index):
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
	arr_group = range(group_size)
	groups.run_simulation(arr_group)

	print("==== Groups after simulation ====")
	for i in range(group_size):
		groups.print_scores(i)

	arr_group = [0,1,2]
	groups.run_simulation(arr_group)
	print("==== Groups after sub-group simulation ====")
	for i in range(group_size):
		groups.print_scores(i)

	arr_priority = [1,1,2]
	groups.set_priority(arr_priority)
	groups.run_simulation(arr_group)

	print("==== Groups after changing priority (sched to teammate) ====")
	for i in range(group_size):
		groups.print_scores(i)

if __name__ == '__main__':
	main()
