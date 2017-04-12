--this is the script that builds our tables for the database

--OH, pk: primary key
--fk: foreign key
--ask Amber for questions

create table users
(user_pk serial primary key,
firstName varchar(16),
lastName varchar(16),
hasATeam BOOLEAN not null default FALSE
);

create table strength(
user_fk integer REFERENCES users (user_pk),
sJava BOOLEAN not null default FALSE,
sCPP BOOLEAN not null default FALSE,
sSQL BOOLEAN not null default FALSE,
sHTML BOOLEAN not null default FALSE,
sPHP BOOLEAN not null default FALSE,
sJavascript BOOLEAN not null default FALSE,
sBash BOOLEAN not null default FALSE,
sGit BOOLEAN not null default FALSE,
sMongo BOOLEAN not null default FALSE,
sWSS BOOLEAN not null default FALSE,
sGIS BOOLEAN not null default FALSE,
sPython BOOLEAN not null default FALSE,
sPMO BOOLEAN not null default FALSE);

create table weakness(
user_fk integer REFERENCES users (user_pk),
wJava BOOLEAN not null default FALSE,
wCPP BOOLEAN not null default FALSE,
wSQL BOOLEAN not null default FALSE,
wHTML BOOLEAN not null default FALSE,
wPHP BOOLEAN not null default FALSE,
wJavascript BOOLEAN not null default FALSE,
wBash BOOLEAN not null default FALSE,
wGit BOOLEAN not null default FALSE,
wMongo BOOLEAN not null default FALSE,
wWSS BOOLEAN not null default FALSE,
wGIS BOOLEAN not null default FALSE,
wPython BOOLEAN not null default FALSE,
wPMO BOOLEAN not null default FALSE);

create table times(
user_fk integer REFERENCES users (user_pk),
mon8to10 BOOLEAN not null default FALSE,
mon10to12 BOOLEAN not null default FALSE,
mon12to2 BOOLEAN not null default FALSE,
mon2to4 BOOLEAN not null default FALSE,
mon4to6 BOOLEAN not null default FALSE,
mon6to8 BOOLEAN not null default FALSE,
tue8to10 BOOLEAN not null default FALSE,
tue10to12 BOOLEAN not null default FALSE,
tue12to2 BOOLEAN not null default FALSE,
tue2to4 BOOLEAN not null default FALSE,
tue4to6 BOOLEAN not null default FALSE,
tue6to8 BOOLEAN not null default FALSE,
wed8to10 BOOLEAN not null default FALSE,
wed10to12 BOOLEAN not null default FALSE,
wed12to2 BOOLEAN not null default FALSE,
wed2to4 BOOLEAN not null default FALSE,
wed4to6 BOOLEAN not null default FALSE,
wed6to8 BOOLEAN not null default FALSE,
thu8to10 BOOLEAN not null default FALSE,
thu10to12 BOOLEAN not null default FALSE,
thu12to2 BOOLEAN not null default FALSE,
thu2to4 BOOLEAN not null default FALSE,
thu4to6 BOOLEAN not null default FALSE,
thu6to8 BOOLEAN not null default FALSE,
fri8to10 BOOLEAN not null default FALSE,
fri10to12 BOOLEAN not null default FALSE,
fri12to2 BOOLEAN not null default FALSE,
fri2to4 BOOLEAN not null default FALSE,
fri4to6 BOOLEAN not null default FALSE,
fri6to8 BOOLEAN not null default FALSE,
sat8to10 BOOLEAN not null default FALSE,
sat10to12 BOOLEAN not null default FALSE,
sat12to2 BOOLEAN not null default FALSE,
sat2to4 BOOLEAN not null default FALSE,
sat4to6 BOOLEAN not null default FALSE,
sat6to8 BOOLEAN not null default FALSE,
sun8to10 BOOLEAN not null default FALSE,
sun10to12 BOOLEAN not null default FALSE,
sun12to2 BOOLEAN not null default FALSE,
sun2to4 BOOLEAN not null default FALSE,
sun4to6 BOOLEAN not null default FALSE,
sun6to8 BOOLEAN not null default FALSE

);

--Max team size is 5 with given table
create table teams(
team_pk serial primary key,
first_fk integer REFERENCES users (user_pk),
second_fk integer REFERENCES users (user_pk),
third_fk integer REFERENCES users (user_pk),
fourth_fk integer REFERENCES users (user_pk),
fifth_fk integer REFERENCES users (user_pk)
);