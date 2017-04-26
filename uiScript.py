#Anisha Aggarwal	 uiScript.py

import cvs

with open('blank.csv', newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	for row in spamreader:
		print(', '.join(row))

def main():


if __name__ == '__main__':
	main()

