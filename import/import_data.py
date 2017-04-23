import csv

def import_users():
        with open("userdata.csv") as f:
                userdata = csv.reader(f, skipinitialspace=True)
                next(userdata)
                #s is each line
                for s in userdata:
                        print("INSERT INTO users (username, teammate) VALUES ('{}', '{}');".format (s[1], s[50]))
                        languages=[s[37],s[38],s[39],s[40],s[41],s[42],s[43],s[44],s[45],s[46], s[47],s[48],s[49]]
                        wordlan=['JAVA', 'CPP', 'SQL', 'HTML', 'PHP', 'Javascript', 'Bash', 'Git', 'Mongo', 'WSS', 'GIS', 'Python', 'PMO']
                        i=0
                        boolan=[]
                        for lan in languages:
                                if lan=='Yes':
                                        boolan.append(wordlan[i])          
                                else:
                                        boolan.append('')
                                i=i+1
                        print("INSERT INTO languages (username, JAVA, CPP, SQL, HTML, PHP, Javascript, Bash,\
                              Git, Mongo, WSS, GIS, Python, PMO) VALUES ('{}', '{}', '{}','{}','{}',\
                              '{}','{}','{}','{}','{}','{}','{}','{}','{}' );".format\
                              (s[1],boolan[0], boolan[1],boolan[2],boolan[3],boolan[4],
                               boolan[5],boolan[6],boolan[7],boolan[8],boolan[9],
                               boolan[10],boolan[11], boolan[12]))
                        times=[s[2],s[3],s[4],s[5],s[6],s[7],s[8],s[9],s[10],s[11],
                               s[12],s[13],s[14],s[15],s[16], s[17],s[18],s[19],s[20],
                               s[21],s[22],s[23],s[24],s[25],s[26],s[27],s[28],s[29],
                               s[30], s[31],s[32],s[33],s[34],s[35],s[36]]
                        
                        scheduals = ["Monday 8 AM to 10 AM", "Monday 10 AM to 12 PM", "Monday 12PM to 2 PM", "Monday 2 PM to 4 PM", "Monday 4 PM to 6 PM",
                        "Tuesday 8 AM to 10 AM", "Tuesday 10 AM to 12 PM", "Tuesday 12 PM to 2 PM", "Tuesday 2 PM to 4 PM", "Tuesday 4 PM to 6 PM",
                        "Wednesday 8 AM to 10 AM", "Wednesday 10 AM to 12 PM", "Wednesday 12 PM to 2 PM", "Wednesday 2 PM to 4 PM", "Wednesday 4 PM to 6 PM",
                        "Thursday 8 AM to 10 AM", "Thursday 10 AM to 12 PM", "Thursday 12 PM to 2 PM", "Thursday 2 PM to 4 PM", "Thursday 4 PM to 6 PM",
                        "Friday 8 AM to 10 AM", "Friday 10 AM to 12 PM", "Friday 12 PM to 2 PM", "Friday 2 PM to 4 PM", "Friday 4 PM to 6 PM",
                        "Saturday 8 AM to 10 AM", "Saturday 10 AM to 12 PM", "Saturday 12 PM to 2 PM", "Saturday 2 PM to 4 PM", "Saturday 4 PM to 6 PM",
                        "Sunday 8 AM to 10 AM", "Sunday 10 AM to 12 PM", "Sunday 12 PM to 2 PM", "Sunday 2 PM to 4 PM", "Sunday 4 PM to 6 PM"]
                        i=0
                        sch=[]
                        for t in times:
                                if t=='yes':
                                        sch.append(i)
                                else:
                                        sch.append(100)
                                i=i+1
                        print("INSERT INTO times (username, mon8to10, mon10to12, mon12to2, mon2to4,mon4to6,tue8to10,\
                              tue10to12,tue12to2,tue2to4,tue4to6) VALUES\
                              ('{}','{}', '{}', '{}','{}','{}','{}','{}','{}','{}','{}'\
                              );".format(s[1],sch[0],sch[1],sch[2],sch[3],sch[4],sch[5],sch[6],sch[7],sch[8],sch[9],sch[10]))

                        # print("INSERT INTO times (username, mon8to10, mon10to12, mon12to2, mon2to4,mon4to6,tue8to10,\
                        #       tue10to12,tue12to2,tue2to4,tue4to6,wed8to10,wed10to12,wed12to2,wed2to4,wed4to6,thu8to10,\
                        #       thu10to12,thu12to2,thu2to4,thu4to6,fri8to10,fri10to12,fri12to2,fri2to4,fri4to6,sat8to10,\
                        #       sat10to12,sat12to2,sat2to4,sat4to6,sun8to10,sun10to12,sun12to2,sun2to4,sun4to6) VALUES\
                        #       ('{}','{}', '{}', '{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',\
                        #       '{}''{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}', '{}' );".format 
                        #       (s[0],sch[0],sch[1],sch[2],sch[3],sch[4],sch[5],sch[6],sch[7],sch[8],sch[9],sch[10],sch[11],sch[12],
                        #        sch[13],sch[14],sch[15],sch[16],sch[17],sch[18],sch[19],sch[20],sch[21],sch[22],sch[23],sch[24],
                        #        sch[25],sch[26],sch[27],sch[28],sch[29],sch[30],sch[31],sch[32],sch[33],sch[34]))
                        






               
if __name__ == "__main__":
        import_users()
