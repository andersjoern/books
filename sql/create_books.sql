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
CREATE TABLE IF NOT EXISTS  book_authors(
  bookid     INTEGER, 
  authorid   INTEGER, 
  FOREIGN KEY(bookid) REFERENCES books(id),
  FOREIGN KEY(authorid) REFERENCES authors(id)  
);
CREATE TABLE IF NOT EXISTS  "books" (
	"id"	INTEGER,
	"publisher"	INTEGER,
	"isbn"	TEXT,
	"edition"	TEXT,
	"title"	TEXT,
	FOREIGN KEY("publisher") REFERENCES "publishers"("id"),
	PRIMARY KEY("id")
);
