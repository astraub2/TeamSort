--this is the script that builds our tables for the database

--OH, pk: primary key
--fk: foreign key
--ask Amber for questions

create table users
(user_pk serial primary key,
username varchar(64),
hasATeam BOOLEAN not null default FALSE)
teammate varchar(64);


create table languages(
user_fk integer REFERENCES users (user_pk),
username varchar(64),
Java varchar(64),
CPP varchar(64),
SQL varchar(64),
HTML varchar(64),
PHP varchar(64),
Javascript varchar(64),
Bash varchar(64),
Git varchar(64),
Mongo varchar(64),
WSS varchar(64),
GIS varchar(64),
Python varchar(64),
PMO varchar(64));


create table times(
username varchar(64),
user_fk integer REFERENCES users (user_pk),
mon8to10 varchar(64),
mon10to12 varchar(64),
mon12to2 varchar(64),
mon2to4 varchar(64),
mon4to6 varchar(64),
mon6to8 varchar(64),
tue8to10 varchar(64),
tue10to12 varchar(64),
tue12to2 varchar(64),
tue2to4 varchar(64),
tue4to6 varchar(64),
tue6to8 varchar(64),
wed8to10 varchar(64),
wed10to12 varchar(64),
wed12to2 varchar(64),
wed2to4 varchar(64),
wed4to6 varchar(64),
wed6to8 varchar(64),
thu8to10 varchar(64),
thu10to12 varchar(64),
thu12to2 varchar(64),
thu2to4 varchar(64),
thu4to6 varchar(64),
thu6to8 varchar(64),
fri8to10 varchar(64),
fri10to12 varchar(64),
fri12to2 varchar(64),
fri2to4 varchar(64),
fri4to6 varchar(64),
fri6to8 varchar(64),
sat8to10 varchar(64),
sat10to12 varchar(64),
sat12to2 varchar(64),
sat2to4 varchar(64),
sat4to6 varchar(64),
sat6to8 varchar(64),
sun8to10 varchar(64),
sun10to12 varchar(64),
sun12to2 varchar(64),
sun2to4 varchar(64),
sun4to6 varchar(64),
sun6to8 varchar(64)

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