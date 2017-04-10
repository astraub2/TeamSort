--this is the script that builds our tables for the database
--users currently has a tone of data
--we might concider breaking it up into 
--a couple tables, ex: a weakness
--strenght a time avaibliy table linked
--to the pk of each user
--OH, pk: primary key
--fk: foreign key
--ask Amber for questions

create table users
(user_pk serial primary key,
firstName varchar(16),
lastName varchar(16),
sJava BOOLEAN not null default 0,
sCPP BOOLEAN not null default 0,
sSQL BOOLEAN not null default 0,
sHTML BOOLEAN not null default 0,
sPHP BOOLEAN not null default 0,
sJavascript BOOLEAN not null default 0,
sBash BOOLEAN not null default 0,
sGit BOOLEAN not null default 0,
sMongo BOOLEAN not null default 0,
sWSS BOOLEAN not null default 0,
sGIS BOOLEAN not null default 0,
sPython BOOLEAN not null default 0,
sPMO BOOLEAN not null default 0,
wJava BOOLEAN not null default 0,
wCPP BOOLEAN not null default 0,
wSQL BOOLEAN not null default 0,
wHTML BOOLEAN not null default 0,
wPHP BOOLEAN not null default 0,
wJavascript BOOLEAN not null default 0,
wBash BOOLEAN not null default 0,
wGit BOOLEAN not null default 0,
wMongo BOOLEAN not null default 0,
wWSS BOOLEAN not null default 0,
wGIS BOOLEAN not null default 0,
wPython BOOLEAN not null default 0,
wPMO BOOLEAN not null default 0,
mon8to10 BOOLEAN not null default 0,
mon10to12 BOOLEAN not null default 0,
mon12to2 BOOLEAN not null default 0,
mon2to4 BOOLEAN not null default 0,
mon4to6 BOOLEAN not null default 0,
mon6to8 BOOLEAN not null default 0,
tue8to10 BOOLEAN not null default 0,
tue10to12 BOOLEAN not null default 0,
tue12to2 BOOLEAN not null default 0,
tue2to4 BOOLEAN not null default 0,
tue4to6 BOOLEAN not null default 0,
tue6to8 BOOLEAN not null default 0,
wed8to10 BOOLEAN not null default 0,
wed10to12 BOOLEAN not null default 0,
wed12to2 BOOLEAN not null default 0,
wed2to4 BOOLEAN not null default 0,
wed4to6 BOOLEAN not null default 0,
wed6to8 BOOLEAN not null default 0,
thu8to10 BOOLEAN not null default 0,
thu10to12 BOOLEAN not null default 0,
thu12to2 BOOLEAN not null default 0,
thu2to4 BOOLEAN not null default 0,
thu4to6 BOOLEAN not null default 0,
thu6to8 BOOLEAN not null default 0,
fri8to10 BOOLEAN not null default 0,
fri10to12 BOOLEAN not null default 0,
fri12to2 BOOLEAN not null default 0,
fri2to4 BOOLEAN not null default 0,
fri4to6 BOOLEAN not null default 0,
fri6to8 BOOLEAN not null default 0,
sat8to10 BOOLEAN not null default 0,
sat10to12 BOOLEAN not null default 0,
sat12to2 BOOLEAN not null default 0,
sat2to4 BOOLEAN not null default 0,
sat4to6 BOOLEAN not null default 0,
sat6to8 BOOLEAN not null default 0,
sun8to10 BOOLEAN not null default 0,
sun10to12 BOOLEAN not null default 0,
sun12to2 BOOLEAN not null default 0,
sun2to4 BOOLEAN not null default 0,
sun4to6 BOOLEAN not null default 0,
sun6to8 BOOLEAN not null default 0,

hasATeam BOOLEAN not null default 0,



);

--Max team size is 5 with given table
create table teams(
team_pk serial primary key,
first_fk integer REFERENCES users (user_pk),
second_fk integer REFERENCES users (user_pk),
third_fk integer REFERENCES users (user_pk),
fourth_fk integer REFERENCES users (user_pk),
fifth_fk integer REFERENCES users (user_pk),

);