CREATE TABLE IF NOT EXISTS "authors" (
	"id"	INTEGER,
	"name"	TEXT,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "publishers" (
	"id"	INTEGER,
	"name"	TEXT,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "books" (
	"id"	INTEGER,
	"author"	INTEGER,
	"publisher"	INTEGER,
	"isbn"	TEXT,
	"edition"	TEXT,
	"title"	TEXT,
	FOREIGN KEY("publisher") REFERENCES "publishers"("id"),
	FOREIGN KEY("author") REFERENCES "authors"("id"),
	PRIMARY KEY("id")
);