import psycopg2
#psycopg2 is our database connector

def main():
	#the var in conn will change, this is temp
	conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cur = conn.cursor()

    #Below is a general query format for database info
    cur.execute('SELECT username FROM users WHERE username=%s;', (username,))
    
    #essentially check if the query returned anything
    try:
        result = cur.fetchone()
    except ProgrammingError:
        result = None
    if result == None:

    else:
    	#result may hold a Boolean, int, string, etc,
    	#check if result is what you want

    #following is a basic insert into DB query

    cur.execute('INSERT INTO roles (role_name) VALUES(%s);',(role,))
         
    #important, anytime the database is updated, like
    #a team is made, we must run following command:
    conn.commit()


if __name__ == "__main__":
	main()