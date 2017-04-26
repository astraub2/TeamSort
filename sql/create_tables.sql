--this is the script that builds our tables for the database

--OH, pk: primary key
--fk: foreign key
--ask Amber for questions

create table users
(user_pk serial primary key,
username varchar(64),
hasATeam BOOLEAN not null default FALSE,
teammate varchar(64)
);


create table languages(
user_fk integer REFERENCES users (user_pk),
username varchar(64),
Java int,
CPP int,
SQL int,
HTML int,
PHP int,
Javascript int,
Bash int,
Git int,
Mongo int,
WSS int,
GIS int,
Python int,
PMO int);


create table times(
username varchar(64),
user_fk integer REFERENCES users (user_pk),
mon8to10 int,
mon10to12 int,
mon12to2 int,
mon2to4 int,
mon4to6 int,
mon6to8 int,
tue8to10 int,
tue10to12 int,
tue12to2 int,
tue2to4 int,
tue4to6 int,
tue6to8 int,
wed8to10 int,
wed10to12 int,
wed12to2 int,
wed2to4 int,
wed4to6 int,
wed6to8 int,
thu8to10 int,
thu10to12 int,
thu12to2 int,
thu2to4 int,
thu4to6 int,
thu6to8 int,
fri8to10 int,
fri10to12 int,
fri12to2 int,
fri2to4 int,
fri4to6 int,
fri6to8 int,
sat8to10 int,
sat10to12 int,
sat12to2 int,
sat2to4 int,
sat4to6 int,
sat6to8 int,
sun8to10 int,
sun10to12 int,
sun12to2 int,
sun2to4 int,
sun4to6 int,
sun6to8 int

);

--Max team size is 5 with given table
create table teams(
team_pk serial primary key,
first_fk integer REFERENCES users (user_pk),
second_fk integer REFERENCES users (user_pk),
third_fk integer REFERENCES users (user_pk),
fourth_fk integer REFERENCES users (user_pk),
fifth_fk integer REFERENCES users (user_pk),
teamIsFull BOOLEAN not null default FALSE

);