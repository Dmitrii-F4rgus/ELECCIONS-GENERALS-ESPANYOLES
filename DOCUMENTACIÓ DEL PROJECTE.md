# DOCUMENTACIÓ DEL PROJECTE

# Configuració i instal·lació de paquets per connectar Python a la base de dades.

Per connectar al Python a la nostra base de dades hem d’utilitzar en el CMD amb permisos  d’administrador la seguent comanda:

```powershell
pip install mysql-connector-pyhton
```

En cas de que la comanda falli pot ser per que la comanda es té que executar en un altre ruta per exemple:

```powershell
cd \users\usuario\AppData\Local\Programs\Python\Python310

C:\users\usuario\AppData\Local\Programs\Python\Python310> -m pip install mysql-connector-pyhton
```

Si tot a anat correctament amb les comandes especifiques es podria fer la comunicacio amb la base de dades.

## Comandes python de la importació

La primera taula que hem d’omplenar per poder començar amb els INSERTS és la taula “eleccions”.

```python
# Connect to the database
cnx = mysql.connector.connect(
    host="10.94.255.163",
    user="perepi",
    password="pastanaga",
    database="eleccions"
)
cursor = cnx.cursor()

# Open the file
with open("02021911.DAT", "r") as file:
    # Read each line of the file
    for line in file:
        # Strip leading and trailing whitespace from the line
        data = line.strip()
        # Extract the values from the data string
        any = data[2:6]
        nom = data[0:2].replace("02", "Elecciones al Congreso de los Diputados") + any  
        mes = data[6:8]
        data = any + "-" + mes + "-" + data[12:14]
        query = "INSERT INTO eleccions (nom, data) VALUES (%s, %s)"
        values = (nom, data)
        cursor.execute(query, values)

# Commit the changes
cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()
```

Ara ja tenim el primer INSERT dintre de la base de dades. La dada “eleccio_id” era necessària per poder continuar ja que fa de FOREIGN KEY en altres taules. 


### Insert de comunitats_autònomes

Un cop fet l’INSERT a la primera taula hem seguit per les comunitats autònomes i les províncies.

Per tal de poder solucionar el problema de la comunitat autònoma “Total Nacional”, la qual porta el codi 99 i no mesclar algunes comunitats amb províncies que porten el mateix nom, hem fet servir el següent programa per poder introduïr les dades.

```python
import mysql.connector

# Connect to the database
cnx = mysql.connector.connect(
    host="10.94.255.163",
    user="perepi",
    password="pastanaga",
    database="eleccions"
)
cursor = cnx.cursor()

# Open the file
with open("07021911.DAT", "r") as file:
    # Read each line of the file
    for line in file:
        # Strip leading and trailing whitespace from the line
        data = line.strip()
        # Extract the values from the data string
        nom = data[14:64].strip().replace("\"", "'")
        codi_ine_prov = data[11:13].replace("\"", "'")
        codi_ine = data[9:11]

        if codi_ine != "99" and codi_ine_prov == "99":
                query = "INSERT INTO comunitats_autonomes (nom, codi_ine) VALUES (%s, %s)"
                values = (nom, codi_ine)
                cursor.execute(query, values)
        else:
            pass
# Commit the changes
cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()
```

Hem fet la part de les comunitats autònomes primer ja que necessitem la dada de comunitat_aut_id, la qual fa de FOREIGN KEY en la taula de províncies. Hem hagut de fer servir un SELECT dins d’un INSERT per poder comparar després els codi_ine i poder triar l’id que li pertany.

### Insert Províncies

```python
import mysql.connector

# Connect to the database
cnx = mysql.connector.connect(
#    host="192.168.56.103",
    host="10.94.255.163",
    user="perepi",
    password="pastanaga",
    database="eleccions"
)
cursor = cnx.cursor()

# Open the file
with open("07021911.DAT", "r") as file:
    # Read each line of the file
    for line in file:
        # Strip leading and trailing whitespace from the line
        data = line.strip()
        # Extract the values from the data string
        nom = data[14:64].replace(" ", "")
        codi_ine = data[11:13].replace("\"", "'")
        num_escons = data[149:155].replace("\"", "'")
        codi_ine_ca = data[9:11].replace("\"", "'")
        IHATEDATSYKA=cursor.execute(f"SELECT comunitat_aut_id FROM comunitats_autonomes WHERE codi_ine = '{line[9:11]}'")# Select
        IHATEDATSYKA = cursor.fetchone()
        if codi_ine_ca != "99" and codi_ine != "99":
            query = "INSERT INTO provincies (comunitat_aut_id, nom, codi_ine, num_escons) VALUES (%s, %s, %s, %s)"
            values = (IHATEDATSYKA[0], nom, codi_ine, num_escons)
            cursor.execute(query, values)
        else:
             pass
        
# Commit the changes
cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()
```

### Insert Municipis

```python
import mysql.connector

# Connect to the database
cnx = mysql.connector.connect(
#    host="192.168.56.103",
    host="10.94.255.163",
    user="perepi",
    password="pastanaga",
    database="eleccions"
)
cursor = cnx.cursor()

# Open the file
with open("05021911.DAT", "r") as file:
    # Read each line of the file
    for line in file:
        # Strip leading and trailing whitespace from the line
        data = line.strip()
        # Extract the values from the data string
        nom = data[18:118].replace(" ", "")
        codi_ine_mu = data[13:16].replace("\"", "'")
        codi_ine_pr = data[11:13].replace("\"", "'")
        districte = data[16:18].replace("\"", "'")
        IHATEDATSYKA=cursor.execute(f"SELECT provincia_id FROM provincies WHERE codi_ine = '{codi_ine_pr}'")# Select
        IHATEDATSYKA = cursor.fetchone()
        query = "INSERT INTO municipis (nom, codi_ine, provincia_id, districte) VALUES (%s, %s, %s, %s)"
        values = (nom, codi_ine_mu, IHATEDATSYKA[0], districte)
        cursor.execute(query, values)
             

# Commit the changes
cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()
```

### Insert Eleccions_municipis

```python

```

### Insert Candidatures

```python

```

### Insert Vots_candidatures_ca

```python

```
Abans de fer el insert de la taula persones tenim que fer alguns canvis a la base de dades (servidor) per aixpo tenim que seguir les instruccions del fitxer "PRIVILEGES FOR DB USER"

### Insert Persones

```python

```

### Insert Candidats(NF)

```python

```

# APARTAT 2

## CONSULTES SIMPLES

1. Volem saber els noms dels municipis que començin per A:
SELECT nom
  FROM municipis
 WHERE nom RLIKE 'A';

1. Volem saber el total de persones que hi han amb sexe masculi:
SELECT sexe, COUNT() AS total
    FROM persones
WHERE sexe='M'
GROUP BY sexe;
**
2. Consulta per saber les eleccions que es varen fer abans del 2000:
**SELECT any 
  FROM eleccions
WHERE any>2000;
**
3. Volem saber la suma de vots totals i agrupar-ho per provincia id:
**SELECT provincia_id, SUM(vots) as vots_totals
    FROM vots_candidatures_prov
GROUP BY provincia_id;
**
4. Consultar el id i el nom de la comunitat autonoma de Andalucia:
SELECT comunitat_aut_id,nom 
  FROM comunitats_autonomes
WHERE nom='Andalucia';

### CONSULTES INNER JOIN

1. /* contar el numero de votos por provincia */
SELECT pro.nom AS provincia, vot.vots AS num_vots 

         FROM provincies pro 

         INNER JOIN vots_candidatures_prov vot ON pro.provincia_id = vot.provincia_id 

2. */ nombres de los candidatos de cada candidatura */
      SELECT can.nom_curt,per.nom AS nom_candidat 

           FROM candidatures can
           INNER JOIN candidats can1 ON can.candidatura_id = can1.candidatura_id
           INNER JOIN persones per ON can1.persona_id = per.persona_id

1. Quins municipis hi ha per cada provincia:
SELECT p.nom AS nom_provincia, m.nom AS nom_municipi
     FROM provincies p
     INNER JOIN municipis m ON m.provincia_id = p.provincia_id;

1. Saber els vots valids i l’any de cada elecció

      SELECT e.eleccio_id,e.any,m.vots_valids
           FROM eleccions e
      LEFT JOIN eleccions_municipis m ON e.eleccio_id = m.eleccio_id

      WHERE vots_valids IS NULL;

1. Quin es el id del primer candidat dels candidats obtinguts per provincia 
SELECT c.candidat_id,p.candidats_obtinguts
FROM vots_candidatures_prov p
RIGHT JOIN candidats c ON p.candidatura_id = c.candidatura_id
LIMIT 1;

## SUBCONSULTES

1. Obté la eleccio_id, el municipi_id i el num de vots vàlids de les eleccions municipals amb més vots en blanc
    
    SELECT eleccio_id, municipi_id, vots_valids
    FROM eleccions_municipis
    WHERE vots_blanc = (SELECT MAX(vots_blanc)
    FROM eleccions_municipis);
    
2. Visualitzar l'id de candidat i el nom del canditat més jove
    
    SELECT c.candidat_id, p.nom
    FROM candidats c
    INNER JOIN persones p ON p.persona_id
    WHERE p.data_naixement=(SELECT MAX(data_naixement)
    FROM persones
    GROUP BY data_naixement);
    
3. Volem saber el número de vots de la canditatura(comunitat autonoma) amb el candidat més vell
    
    SELECT v.vots
    FROM vots_candidatures_ca v
    INNER JOIN candidats c ON c.candidatura_id=v.candidatura_id
    INNER JOIN persones p ON c.persona_id=p.persona_id
    WHERE p.data_naixement=(SELECT MIN(data_naixement)
    FROM persones);
    
4. Volem saber els candidats que són més joves que el que marca la mitja d'edat
    
    SELECT *
    FROM persones
    WHERE data_naixement>(SELECT AVG(data_naixement)
    FROM persones);
    
5. Obté el nom del municipi, el seu id, el numero de vots a candidatures i el total de vots emeoss del municipi que hagi tingut més vots nuls
    
    
    SELECT m.nom, e.municipi_id, e.vots_candidatures, e.vots_emesos
    FROM eleccions_municipis e
    INNER JOIN municipis m ON e.municipi_id=m.municipi_id
    WHERE vots_nuls=(SELECT MAX(vots_nuls)
    FROM eleccions_municipis);
    

# APARTAT 3

# **APARTAT 5**

**1.5 Llei d’Hondt**

La fórmula D'Hondt es el procediment matematic que s’utilitza per distribuir els escons entre les candidatures a partir dels vots

EXEMPLE: municipi amb 9 regidors a repartir i 10 candidatures, i en el qual s’hane emès 1400 vots vàlids,de la seguent manera:


En cas d'empat en algun quocient, s'emporta l'escó la candidatura que té més vots en total.

PROGRAMA QUE MOSTRA EL NUMERO D’ESCONS