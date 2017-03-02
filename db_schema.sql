drop table if exists url;
CREATE TABLE url(
	"id" INTEGER PRIMARY KEY autoincrement,
	"ip" varchar(255),
	"score" varchar(255)
);