import mysql.connector
print("START")
# Connect to the database
cnx = mysql.connector.connect(
    host="192.168.56.103",
#    host="10.94.255.163",
    user="perepi",
    password="pastanaga",
    database="sys"
)
cursor = cnx.cursor()

cursor.execute(" CREATE DATABASE eleccions;")
cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()
cnx = mysql.connector.connect(
    host="192.168.56.103",
#    host="10.94.255.163",
    user="perepi",
    password="pastanaga",
    database="eleccions"
)
cursor = cnx.cursor()
cursor.execute("""
                    -- -----------------------------------------------------
                    -- Table comunitats
                    -- -----------------------------------------------------
                    CREATE TABLE comunitats_autonomes (
                      comunitat_aut_id TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
                      nom VARCHAR(45) NULL,
                      codi_ine CHAR(2) NOT NULL,
                      PRIMARY KEY (comunitat_aut_id)
                    ); """)


# Commit the changes
cnx.commit()
cursor.execute("""
                    -- -----------------------------------------------------
                    -- Table provincies
                    -- -----------------------------------------------------
                    CREATE TABLE provincies (
                      provincia_id TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
                      comunitat_aut_id TINYINT UNSIGNED NOT NULL,
                      nom VARCHAR(45) NULL,
                      codi_ine CHAR(2) NOT NULL,
                      num_escons TINYINT UNSIGNED NULL,
                      PRIMARY KEY (provincia_id),
                      CONSTRAINT fk_provincies_comunitats_autonomes
                        FOREIGN KEY (comunitat_aut_id)
                        REFERENCES comunitats_autonomes (comunitat_aut_id)
                        );""")
cnx.commit()
cursor.execute("""
                    -- -----------------------------------------------------
                    -- Table municipis
                    -- -----------------------------------------------------
                    CREATE TABLE municipis (
                      municipi_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
                      nom VARCHAR(100) NULL,
                      codi_ine CHAR(3) NOT NULL,
                      provincia_id TINYINT UNSIGNED NOT NULL,
                      districte CHAR(2) NULL,
                      PRIMARY KEY (municipi_id),
                      CONSTRAINT fk_municipis_provincies
                        FOREIGN KEY (provincia_id)
                        REFERENCES provincies (provincia_id)
                        );""")
cnx.commit()
cursor.execute("""
                    -- -----------------------------------------------------
                    -- Table eleccions
                    -- -----------------------------------------------------
                    CREATE TABLE eleccions (
                      eleccio_id TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
                      nom VARCHAR(45) NULL,
                      data DATE NOT NULL,
                      any YEAR GENERATED ALWAYS AS (YEAR(data)),
                      mes TINYINT GENERATED ALWAYS AS (MONTH(data)),
                      PRIMARY KEY (eleccio_id)
                      );
                    """)

cnx.commit()
cursor.execute("""
                    -- -----------------------------------------------------
                    -- Table eleccions_municipis
                    -- -----------------------------------------------------
                    CREATE TABLE eleccions_municipis (
                      eleccio_id TINYINT UNSIGNED NOT NULL,
                      municipi_id SMALLINT UNSIGNED NOT NULL,
                      num_meses SMALLINT UNSIGNED NULL,
                      cens INT UNSIGNED NULL,
                      vots_emesos INT UNSIGNED NULL, 
                      vots_valids INT UNSIGNED NULL, 
                      vots_candidatures INT UNSIGNED NULL,
                      vots_blanc INT UNSIGNED NULL,
                      vots_nuls INT UNSIGNED NULL,
                      PRIMARY KEY (eleccio_id, municipi_id),
                      CONSTRAINT fk_eleccions_municipis_municipis
                        FOREIGN KEY (municipi_id)
                        REFERENCES municipis (municipi_id),
                      CONSTRAINT fk_eleccions_municipis_eleccions
                        FOREIGN KEY (eleccio_id)
                        REFERENCES eleccions (eleccio_id)
                    ); """)

cnx.commit()
cursor.execute("""
                    -- -----------------------------------------------------
                    -- Table candidatures
                    -- -----------------------------------------------------
                    CREATE TABLE candidatures (
                      candidatura_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
                      eleccio_id TINYINT UNSIGNED,
                      codi_candidatura CHAR(6) NULL,
                      nom_curt VARCHAR(50) NULL,
                      nom_llarg VARCHAR(150) NULL,
                      codi_acumulacio_provincia CHAR(6) NULL,
                      codi_acumulacio_ca CHAR(6) NULL,
                      codi_acumulario_nacional CHAR(6) NULL,
                      PRIMARY KEY (candidatura_id),
                      CONSTRAINT fk_eleccions_partits_eleccions
                        FOREIGN KEY (eleccio_id)
                        REFERENCES eleccions (eleccio_id)
                            );""")

cnx.commit()
cursor.execute("""
                    -- -----------------------------------------------------
                    -- Table persones
                    -- -----------------------------------------------------
                    CREATE TABLE persones (
                      persona_id INT UNSIGNED NOT NULL,
                      nom VARCHAR(30) NULL,
                      cog1 VARCHAR(30) NULL,
                      cog2 VARCHAR(30) NULL,
                      sexe ENUM('M', 'F') NULL,
                      data_naixement DATE NULL,
                      dni CHAR(10) NOT NULL,
                      PRIMARY KEY (persona_id));""")

cnx.commit()
cursor.execute("""
                    -- -----------------------------------------------------
                    -- Table candidats
                    -- -----------------------------------------------------
                    CREATE TABLE candidats (
                      candidat_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
                      candidatura_id INT UNSIGNED NOT NULL,
                      persona_id INT UNSIGNED NOT NULL,
                      provincia_id TINYINT UNSIGNED NOT NULL,
                      num_ordre TINYINT NULL,
                      tipus ENUM('T', 'S') NULL,
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
                        );""")

cnx.commit()
cursor.execute("""
                    -- -----------------------------------------------------
                    -- Table vots_candidatures_mun
                    -- -----------------------------------------------------
                    CREATE TABLE vots_candidatures_mun (
                      eleccio_id TINYINT UNSIGNED NOT NULL,
                      municipi_id SMALLINT UNSIGNED NOT NULL,
                      candidatura_id INT UNSIGNED NOT NULL,
                      vots INT UNSIGNED NULL,
                      PRIMARY KEY (eleccio_id,municipi_id,candidatura_id),
                      CONSTRAINT fk_candidatures_municipis_candidatures1
                        FOREIGN KEY (candidatura_id)
                        REFERENCES candidatures (candidatura_id),
                      CONSTRAINT fk_candidatures_municipis_eleccions_municipis1
                        FOREIGN KEY (eleccio_id , municipi_id)
                        REFERENCES eleccions_municipis (eleccio_id,municipi_id)
                        );""")

cnx.commit()
cursor.execute("""
                    -- -----------------------------------------------------
                    -- Table vots_candidatures_prov
                    -- -----------------------------------------------------
                    CREATE TABLE vots_candidatures_prov (
                      provincia_id TINYINT UNSIGNED NOT NULL,
                      candidatura_id INT UNSIGNED NOT NULL,
                      vots INT UNSIGNED NULL,
                      candidats_obtinguts SMALLINT UNSIGNED NULL,
                      PRIMARY KEY (provincia_id, candidatura_id),
                      CONSTRAINT fk_candidatures_provincies_provincies1
                        FOREIGN KEY (provincia_id)
                        REFERENCES provincies (provincia_id),
                      CONSTRAINT fk_candidatures_provincies_candidatures1
                        FOREIGN KEY (candidatura_id)
                        REFERENCES candidatures (candidatura_id)
                        );""")
cnx.commit()
cursor.execute("""
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
                        );""")
cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()
print("DONE")
