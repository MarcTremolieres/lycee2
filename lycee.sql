SET time_zone = "+00:00";

USE lycee;


CREATE TABLE Classes (
	id_classe int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	Nom varchar(20) COLLATE utf8_bin NOT NULL,
	Niveau varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE Eleves (
	id_eleve int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	Nom varchar(30) COLLATE utf8_bin NOT NULL,
	Prenom varchar(30) COLLATE utf8_bin NOT NULL,
	id_classe int(11) NOT NULL,
	FOREIGN KEY (id_classe) REFERENCES Classes(id_classe)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;


CREATE TABLE Disciplines (
	id_discipline int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	Nom varchar(30) COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE Profs (
	id_prof int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	Nom varchar(30) COLLATE utf8_bin NOT NULL,
	Prenom varchar(30) COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE Notes (
	id_note int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	id_eleve int(11) NOT NULL,
	id_discipline int(11)NOT NULL,
	id_prof int(11) NOT NULL,
	Date_note datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
	Note int(11),
	FOREIGN KEY (id_eleve) REFERENCES Eleves(id_eleve),
	FOREIGN KEY (id_discipline) REFERENCES Disciplines(id_discipline),
	FOREIGN KEY (id_prof) REFERENCES Profs(id_prof)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;




