CREATE TABLE Staff (
    ID int NOT NULL,
    StaffName varchar(255) NOT NULL,
    Education varchar(255) NOT NULL,
    Skills varchar(255) NOT NULL,
    Experience int NOT NULL,
    PRIMARY KEY (ID)
);

CREATE TABLE Horaire (
    ID int NOT NULL ,
    StaffID int NOT NULL,
    Jour date NOT NULL,
    StartTime time NOT NULL,
    EndTime time NOT NULL,
    PRIMARY KEY (ID),
    FOREIGN KEY (StaffID) REFERENCES Staff(ID) 
);

INSERT INTO Staff VALUES (1, "Name1", "Edu1", "Sk1", 1);
INSERT INTO Staff VALUES (2, "Name2", "Edu2", "Sk2", 2);
INSERT INTO Staff VALUES (3, "Name3", "Edu3", "Sk3", 3);
INSERT INTO Staff VALUES (4, "Name4", "Edu4", "Sk4", 4);
INSERT INTO Staff VALUES (5, "Name5", "Edu5", "Sk5", 5);

INSERT INTO Horaire VALUES (1, 4, '2022-10-23', '9:00', '15:00');
INSERT INTO Horaire VALUES (2, 3, '2022-10-23', '9:00', '15:00');
INSERT INTO Horaire VALUES (3, 1, '2022-10-24', '8:00', '16:00');
INSERT INTO Horaire VALUES (4, 2, '2022-10-24', '8:00', '16:00');
INSERT INTO Horaire VALUES (5, 1, '2022-10-25', '8:00', '16:00');
INSERT INTO Horaire VALUES (6, 2, '2022-10-25', '8:00', '16:00');
INSERT INTO Horaire VALUES (7, 1, '2022-10-26', '8:00', '16:00');
INSERT INTO Horaire VALUES (8, 2, '2022-10-26', '8:00', '16:00');
INSERT INTO Horaire VALUES (9, 1, '2022-10-27', '8:00', '16:00');
INSERT INTO Horaire VALUES (10, 2, '2022-10-27', '8:00', '16:00');
INSERT INTO Horaire VALUES (11, 1, '2022-10-28', '8:00', '16:00');
INSERT INTO Horaire VALUES (12, 2, '2022-10-28', '8:00', '16:00');
INSERT INTO Horaire VALUES (13, 5, '2022-10-29', '9:00', '15:00');
INSERT INTO Horaire VALUES (14, 3, '2022-10-23', '9:00', '15:00');