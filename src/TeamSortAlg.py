#!/usr/bin/env python3

# Vinitha Gadiraju
# Algorithm

import random
import time
import pdb
import copy
import json

# Using static data.  Set this to false to use data from database
TEST_DATA = True

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

				for i in group[G_NDX_USERS][user][U_NDX_PREF]:
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
		"""
		arr_group is an array of the groups that need to be run.
		By default, this includes all groups. However, if the user only wants re-run specific groups, arr-group will be changed.
		For example, if I have 5 groups, arr_group will look like this: 
		[0,1,2,3,4] 
		Let's say I don't like how the first 3 groups were sorted and I want to re-run them. The user will select these groups in the UI and arr_group will be changed to:
		[0,1,2]
		"""
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
	random.seed(int(time.time()))
	#n = int(input("Enter the number of groups: ")) #WE NEED TO GET n FROM THE DATABASE 
	groups = Groups(n)
	group_size = groups.get_size()
	groups.run_simulation(arr_group)

#DEBUG CODE FOR TEST DATA 
#pdb.set_trace()
"""
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
	groups.set_priority(arr_priority)
	groups.run_simulation(arr_group)

	print("==== Groups after changing priority (sched to teammate) ====")
	for i in range(group_size):
		groups.print_groups_scores(i)
"""
if __name__ == '__main__':
	main()
