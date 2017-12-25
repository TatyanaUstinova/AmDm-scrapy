CREATE TABLE artists(
	id serial PRIMARY KEY,
	"name" TEXT UNIQUE NOT NULL 
);

CREATE TABLE songs(
	id serial PRIMARY KEY,
	artist_id INT NOT NULL REFERENCES artists(id),
	"name" TEXT NOT NULL,
	"text" TEXT NOT NULL
);
