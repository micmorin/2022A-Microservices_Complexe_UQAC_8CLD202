CREATE TABLE  profil (
	id	INTEGER NOT NULL AUTO_INCREMENT,
	description	VARCHAR(120) NOT NULL,
	PRIMARY KEY(id)
);
CREATE TABLE users (
	id	INTEGER NOT NULL AUTO_INCREMENT,
	name	VARCHAR(120) NOT NULL,
	username	VARCHAR(120) NOT NULL,
	email	VARCHAR(120) NOT NULL,
	password	VARCHAR(120) NOT NULL,
	token	VARCHAR(120) NOT NULL,
	profil_id	INTEGER NOT NULL,
	PRIMARY KEY(id),
	UNIQUE(username),
	UNIQUE(email),
	FOREIGN KEY(profil_id) REFERENCES profil(id)
);
CREATE TABLE calcul (
	id	INTEGER NOT NULL AUTO_INCREMENT,
	body	VARCHAR(120) NOT NULL,
	result	INTEGER,
	date	DATE NOT NULL,
	user_id	INTEGER NOT NULL,
	PRIMARY KEY(id),
	FOREIGN KEY(user_id) REFERENCES users(id)
);
INSERT INTO profil VALUES (1,'admin');
INSERT INTO profil VALUES (2,'user');
INSERT INTO users VALUES (1,'admin_nom','admin','admin@example.com','pbkdf2:sha256:260000$1jSffTrWttV0Gld3$0cf28460f1afc048b5aed69a797626a81f0d06d0d81ca063ee6d77bb35dbdc24','pbkdf2:sha256:260000$yeoRsL644ky5Kuii$a754ab49545d32b0487e2fa9abfcbd8bdfb0aa05d9dde126bd48b2825bfcc640',1);
INSERT INTO users VALUES (2,'user_nom','user','guest@example.com','pbkdf2:sha256:260000$g3dOQjbUNjWZsmym$ce8788585e49a00cc313b36bdb9ed8a3245a159006a03aa51effc4018ccdcfc4','pbkdf2:sha256:260000$iP8Xg1Mkm0FHiUIT$148bece31167a593e93b919c9de55cb2dff46597a6d3fff833479dc43fe7592f',2);
INSERT INTO calcul VALUES (2,'1+2',3,'2022-09-25',1);
INSERT INTO calcul VALUES (3,'1+3',4,'2022-09-25',2);