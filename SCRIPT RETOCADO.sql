
DROP DATABASE eleccions;

-- -----------------------------------------------------
-- Schema eleccions
-- -----------------------------------------------------

CREATE DATABASE eleccions;
USE eleccions;

-- -----------------------------------------------------
-- Table comunitats
-- -----------------------------------------------------
CREATE TABLE comunitats_autonomes (
  comunitat_aut_id TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
  nom VARCHAR(45) NULL,
  codi_ine CHAR(2) NOT NULL,
  PRIMARY KEY (comunitat_aut_id)
);


-- -----------------------------------------------------
-- Table provincies
-- -----------------------------------------------------
CREATE TABLE provincies (
  provincia_id TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
  comunitat_aut_id TINYINT UNSIGNED NOT NULL,
  nom VARCHAR(45) NULL,
  codi_ine CHAR(2) NOT NULL,
  num_escons TINYINT UNSIGNED NULL COMMENT 'Numero d\'escons que li pertoquen a aquella provincia',
  PRIMARY KEY (provincia_id),
  CONSTRAINT fk_provincies_comunitats_autonomes
    FOREIGN KEY (comunitat_aut_id)
    REFERENCES comunitats_autonomes (comunitat_aut_id)
    );



-- -----------------------------------------------------
-- Table municipis
-- -----------------------------------------------------
CREATE TABLE municipis (
  municipi_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
  nom VARCHAR(100) NULL,
  codi_ine CHAR(3) NOT NULL,
  provincia_id TINYINT UNSIGNED NOT NULL,
  districte CHAR(2) NULL COMMENT 'Número de districte municipal , sinó el seu valor serà 99. Per exemple aquí municiís com Blanes el seu valor serà 99, però en ciutats com Barcelona hi haurà el número de districte',
  PRIMARY KEY (municipi_id),
  CONSTRAINT fk_municipis_provincies
    FOREIGN KEY (provincia_id)
    REFERENCES provincies (provincia_id)
    );


-- -----------------------------------------------------
-- Table eleccions
-- -----------------------------------------------------
CREATE TABLE eleccions (
  eleccio_id TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
  nom VARCHAR(45) NULL,
  data DATE NOT NULL COMMENT 'Data (dia mes i any) de quan s\'han celebrat les eleccions',
  any YEAR GENERATED ALWAYS AS (YEAR(data))  COMMENT 'any el qual s\'han celebrat les eleccions',
  mes TINYINT GENERATED ALWAYS AS (MONTH(data)) STORED COMMENT 'El mes que s\'han celebrat les eleccions',
  PRIMARY KEY (eleccio_id)
  );



-- -----------------------------------------------------
-- Table eleccions_municipis
-- -----------------------------------------------------
CREATE TABLE eleccions_municipis (
  eleccio_id TINYINT UNSIGNED NOT NULL,
  municipi_id SMALLINT UNSIGNED NOT NULL,
  num_meses SMALLINT UNSIGNED NULL,
  cens INT UNSIGNED NULL,
  vots_emesos INT UNSIGNED NULL COMMENT 'Número total de vots realitzats en el municipi',
  vots_valids INT UNSIGNED NULL COMMENT 'Número de vots es que tindran en compte: vots a candidatures + vots nuls',
  vots_candidatures INT UNSIGNED NULL COMMENT 'Total de vots a les candidatures\n',
  vots_blanc INT UNSIGNED NULL,
  vots_nuls INT UNSIGNED NULL,
  PRIMARY KEY (eleccio_id, municipi_id),
  CONSTRAINT fk_eleccions_municipis_municipis
    FOREIGN KEY (municipi_id)
    REFERENCES municipis (municipi_id),
  CONSTRAINT fk_eleccions_municipis_eleccions
    FOREIGN KEY (eleccio_id)
    REFERENCES eleccions (eleccio_id)
);



-- -----------------------------------------------------
-- Table candidatures
-- -----------------------------------------------------
CREATE TABLE candidatures (
  candidatura_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  eleccio_id TINYINT UNSIGNED,
  codi_candidatura CHAR(6) NULL,
  nom_curt VARCHAR(50) NULL COMMENT 'Sigles de la candidatura',
  nom_llarg VARCHAR(150) NULL COMMENT 'Nom llarg de la candidatura (denominació)',
  codi_acumulacio_provincia CHAR(6) NULL COMMENT 'Codi de la candidatura d\'acumulació a nivell provincial.',
  codi_acumulacio_ca CHAR(6) NULL COMMENT 'Codi de la candidatura d\'acumulació a nivell de comunitat autònoma',
  codi_acumulario_nacional CHAR(6) NULL,
  PRIMARY KEY (candidatura_id),
  CONSTRAINT fk_eleccions_partits_eleccions
    FOREIGN KEY (eleccio_id)
    REFERENCES eleccions (eleccio_id)
	);



-- -----------------------------------------------------
-- Table persones
-- -----------------------------------------------------
CREATE TABLE persones (
  persona_id INT UNSIGNED NOT NULL,
  nom VARCHAR(30) NULL,
  cog1 VARCHAR(30) NULL,
  cog2 VARCHAR(30) NULL,
  sexe ENUM('M', 'F') NULL COMMENT 'M=Masculí, F=Femení',
  data_naixement DATE NULL,
  dni CHAR(10) NOT NULL,
  PRIMARY KEY (persona_id));


-- -----------------------------------------------------
-- Table candidats
-- -----------------------------------------------------
CREATE TABLE candidats (
  candidat_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  candidatura_id INT UNSIGNED NOT NULL,
  persona_id INT UNSIGNED NOT NULL,
  provincia_id TINYINT UNSIGNED NOT NULL,
  num_ordre TINYINT NULL COMMENT 'Num ordre del candidatdins la llista del partit dins de la circumpscripció que es presenta.',
  tipus ENUM('T', 'S') NULL COMMENT 'T=Titular, S=Suplent',
  PRIMARY KEY (candidat_id),
  CONSTRAINT fk_candidats_provincies1
    FOREIGN KEY (provincia_id)
    REFERENCES provincies (provincia_id),
  CONSTRAINT fk_candidats_persones1
    FOREIGN KEY (persona_id)
    REFERENCES persones (persona_id),
  CONSTRAINT fk_candidats_candidatures1
    FOREIGN KEY (candidatura_id)
    REFERENCES candidatures(candidatura_id)
    );


-- -----------------------------------------------------
-- Table vots_candidatures_mun
-- -----------------------------------------------------
CREATE TABLE vots_candidatures_mun (
  eleccio_id TINYINT UNSIGNED NOT NULL,
  municipi_id SMALLINT UNSIGNED NOT NULL,
  candidatura_id INT UNSIGNED NOT NULL,
  vots INT UNSIGNED NULL COMMENT 'Número de vots obtinguts per la candidatura',
  PRIMARY KEY (eleccio_id,municipi_id,candidatura_id),
  CONSTRAINT fk_candidatures_municipis_candidatures1
    FOREIGN KEY (candidatura_id)
    REFERENCES candidatures (candidatura_id),
  CONSTRAINT fk_candidatures_municipis_eleccions_municipis1
    FOREIGN KEY (eleccio_id , municipi_id)
    REFERENCES eleccions_municipis (eleccio_id,municipi_id)
    );


-- -----------------------------------------------------
-- Table vots_candidatures_prov
-- -----------------------------------------------------
CREATE TABLE vots_candidatures_prov (
  provincia_id TINYINT UNSIGNED NOT NULL,
  candidatura_id INT UNSIGNED NOT NULL,
  vots INT UNSIGNED NULL COMMENT 'Número de vots obtinguts per la candidatura',
  candidats_obtinguts SMALLINT UNSIGNED NULL COMMENT 'Número de candidats obtinguts per la candidatura',
  PRIMARY KEY (provincia_id, candidatura_id),
  CONSTRAINT fk_candidatures_provincies_provincies1
    FOREIGN KEY (provincia_id)
    REFERENCES provincies (provincia_id),
  CONSTRAINT fk_candidatures_provincies_candidatures1
    FOREIGN KEY (candidatura_id)
    REFERENCES candidatures (candidatura_id)
    );


-- -----------------------------------------------------
-- Table vots_candidatures_ca
-- -----------------------------------------------------
CREATE TABLE vots_candidatures_ca (
  comunitat_autonoma_id TINYINT UNSIGNED NOT NULL,
  candidatura_id INT UNSIGNED NOT NULL,
  vots INT UNSIGNED NULL,
  PRIMARY KEY (comunitat_autonoma_id, candidatura_id),
  CONSTRAINT fk_comunitats_autonomes_has_candidatures_comunitats_autonomes1
    FOREIGN KEY (comunitat_autonoma_id)
    REFERENCES comunitats_autonomes (comunitat_aut_id),
  CONSTRAINT fk_comunitats_autonomes_has_candidatures_candidatures1
    FOREIGN KEY (candidatura_id)
    REFERENCES candidatures(candidatura_id)
    );


