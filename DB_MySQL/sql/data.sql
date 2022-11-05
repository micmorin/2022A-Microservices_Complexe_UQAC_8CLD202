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

CREATE TABLE objet_registration (
	id	INTEGER NOT NULL AUTO_INCREMENT,
	nom VARCHAR(120) NOT NULL,
	token	VARCHAR(120) NOT NULL,
	type_obj	VARCHAR(120) NOT NULL,
	date_reg	DATE NOT NULL,
	status_reg INTEGER NOT NULL,
	PRIMARY KEY(id),
	UNIQUE(token)
);

INSERT INTO profil VALUES (1,'admin');
INSERT INTO profil VALUES (2,'user');
INSERT INTO users VALUES (1,'admin_nom','admin','admin@example.com','pbkdf2:sha256:260000$1jSffTrWttV0Gld3$0cf28460f1afc048b5aed69a797626a81f0d06d0d81ca063ee6d77bb35dbdc24','pbkdf2:sha256:260000$yeoRsL644ky5Kuii$a754ab49545d32b0487e2fa9abfcbd8bdfb0aa05d9dde126bd48b2825bfcc640',1);
INSERT INTO users VALUES (2,'user_nom','user','guest@example.com','pbkdf2:sha256:260000$g3dOQjbUNjWZsmym$ce8788585e49a00cc313b36bdb9ed8a3245a159006a03aa51effc4018ccdcfc4','pbkdf2:sha256:260000$iP8Xg1Mkm0FHiUIT$148bece31167a593e93b919c9de55cb2dff46597a6d3fff833479dc43fe7592f',2);
INSERT INTO objet_registration VALUES (1,'Camera St. Paul','123','Camera','2022-11-01',0);
INSERT INTO objet_registration VALUES (2,'Camera Talbot','456','Camera','2022-11-02',1);
INSERT INTO objet_registration VALUES (3,'Camera Universite','789','Camera','2022-11-03',1);
INSERT INTO objet_registration VALUES (4,'Sonde Jonquiere','012','Sonde_Niveau_Eau','2022-09-03',0);
INSERT INTO objet_registration VALUES (5,'Sonde Chicoutimi','345','Sonde_Niveau_Eau','2022-09-03',1);