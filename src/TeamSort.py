import psycopg2
#psycopg2 is our database connector

def main():
        conn = psycopg2.connect(dbname='teamsort')
        cur = conn.cursor()

        #Below is a general query format for database info
        cur.execute('SELECT username FROM users;')
        #Lets grab all of the usernames for the database:

        #essentially check if the query returned anything
        try:
            result = cur.fetchall()
        except ProgrammingError:
            result = None
        if result == None:
            print("nothing")

        else:
            for i in result:
                #this prints only the string value of the name
                print(i[0])
            

        #   #result may hold a Boolean, int, string, etc,
        #   #check if result is what you want

        # #following is a basic insert into DB query

        # #cur.execute('INSERT INTO roles (role_name) VALUES(%s);',(role,))
         
        # #important, anytime the database is updated, like
        # #a team is made, we must run following command:
        # conn.commit()


if __name__ == "__main__":
    main()
