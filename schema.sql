drop table if exists entries;
create table entries (
	id integer primary key autoincrement,
	title text not null,
	text text not null
);

create table directories (
	id integer primary key autoincrement,
	name text not null,
	children integer not null
);

create table phoneNumbers (
	id integer primary key autoincrement,
	name text not null,
	phoneNum text not null
);