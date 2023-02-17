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

### Insert de Eleccions

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

### Insert Candidatures

```python
import mysql.connector

# Connect to the database
cnx = mysql.connector.connect(
# localhost="192.168.56.103",
    host="10.94.255.163",
    user="perepi",
    password="pastanaga",
    database="eleccions"
)
cursor = cnx.cursor()

# Open the file
with open("03021911.DAT", "r") as file:
    # Read each line of the file
    for line in file:
        # Strip leading and trailing whitespace from the line
        data = line.strip()
        # Extract the values from the data string
        eleccio_id = 1
        codi_candidatura = data[8:14].replace("\"", "'")
        nom_curt = data[14:64].strip().replace("\"", "'")
        nom_llarg = data[64:214].strip().replace("\"", "'")
        codi_acumulacio_provincia = data[214:220].replace("\"", "'")
        codi_acumulacio_ca = data[220:226].replace("\"", "'")
        codi_acumulario_nacional = data[226:232].replace("\"", "'")
        query = "INSERT INTO candidatures (eleccio_id, codi_candidatura, nom_curt, nom_llarg, codi_acumulacio_provincia, codi_acumulacio_ca, codi_acumulario_nacional) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (eleccio_id, codi_candidatura, nom_curt, nom_llarg, codi_acumulacio_provincia, codi_acumulacio_ca, codi_acumulario_nacional)
        cursor.execute(query, values)

# Commit the changes
cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()
```

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

Amb aquest codi extraeiem els valors de les variables nom,cog1,cog2,sexe,data_naixament dni. Despres verifiquem si la data de naixament es correcte tal que aixi "0000-00-00" i si el nom complet no esta duplicat. Si es compleixen totes aquestes condicions insertas els valors a la tabla persones. També hi habia un registre que te cometes("") i per tant habiem de fer que el programa no agafessi les cometes.

### Insert Persones

```python
import mysql.connector
print("START")
# Connect to the database
cnx = mysql.connector.connect(
    host="192.168.56.107",
#    host="10.94.255.163",
    user="perepi",
    password="pastanaga",
    database="eleccions"
)
cursor = cnx.cursor()
contador = 0
# Open the file
full_name_list= ["START"]
with open("04021911.DAT", "r") as file:
    # Read each line of the file
    for line in file:
        # Strip leading and trailing whitespace from the line
        data = line.strip()
        # Extract the values from the data string
        persona_id = contador=contador+1
        nom = data[25:50].strip().replace("\"", "")
        cog1 = data[50:75].strip().replace("\"", "")
        cog2 = data[75:100].strip().replace("\"", "")
        sexe = data[100:101].replace("\"", "'")
        DAY_naixement = data[101:103]
        MES_naixement = data[103:105]
        ANO_naixement = data[105:109]
        data_naixement = ANO_naixement + "-" + MES_naixement + "-" + DAY_naixement 
        dni = data[109:119].strip()
        full_name = f"{nom} {cog1} {cog2}"
        full_name_list.append(full_name)
        if data_naixement == "0000-00-00" and full_name_list.count(full_name) < 2:
                query = "INSERT INTO persones (persona_id, nom, cog1, cog2, sexe, data_naixement, dni) VALUES (%s, %s, %s, %s, %s, %s, %s)"        
                values = (persona_id, nom, cog1, cog2, sexe, None, dni)
                cursor.execute(query, values)
        elif data_naixement != "0000-00-00" and full_name_list.count(full_name) < 2:
                query = "INSERT INTO persones (persona_id, nom, cog1, cog2, sexe, data_naixement, dni) VALUES (%s, %s, %s, %s, %s, %s, %s)"        
                values = (persona_id, nom, cog1, cog2, sexe, data_naixement, dni)
                cursor.execute(query, values)
        else:
                pass
                
# Commit the changes
cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()
print("DONE")

```
El següent codi es per insertar valors a la tabla municipis. No es hem posat municipi_id perque es una clau primaria autoIncremental. Després fiquem les variables i hem de fer 1 SELECT per obtenir el codi_ine de provincies

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
import mysql.connector
print("START")
# Connect to the database
cnx = mysql.connector.connect(
    host="192.168.56.103",
#    host="10.94.255.163",
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
        num_meses = data[136:141]
        cens = data[141:149]
        vots_candidatures = data[205:213]
        vots_candidatures = int(vots_candidatures)
        vots_blanc = data[189:197]
        vots_blanc = int(vots_blanc)
        vots_nuls = data[197:205]
        vots_nuls = int(vots_nuls)
        vots_emesos = vots_candidatures + vots_blanc + vots_nuls
        vots_emesos = int(vots_emesos)
        vots_valids = vots_emesos - vots_nuls
        vots_valids = int(vots_valids)
        codi_ine_mu = data[13:16]
        codi_ine_prov = data[11:13].replace("\"", "'")
        any = data[2:6]
        mes = data[6:8]
        codi_dstrc = data[16:18]
        provincia_id=cursor.execute(f"SELECT provincia_id FROM provincies WHERE codi_ine = '{codi_ine_prov}'")# Select
        provincia_id = cursor.fetchone()
        municipi_id=cursor.execute(f"SELECT municipi_id FROM municipis WHERE codi_ine = '{codi_ine_mu}' AND provincia_id = '{provincia_id[0]}' AND districte = '{codi_dstrc}'")# Select
        municipi_id = cursor.fetchone()
        eleccio_id=cursor.execute(f"SELECT eleccio_id FROM eleccions WHERE any = '{any}' AND mes = '{mes}'")# Select
        eleccio_id = cursor.fetchone()
        query = "INSERT INTO eleccions_municipis (eleccio_id, municipi_id, num_meses, cens, vots_emesos, vots_valids, vots_candidatures, vots_blanc, vots_nuls) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (eleccio_id[0], municipi_id[0], num_meses, cens, vots_emesos, vots_valids, vots_candidatures, vots_blanc, vots_nuls)
        cursor.execute(query, values)

# Commit the changes
cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()
print("DONE")
```

### Insert Candidats

```python
import mysql.connector
print("START")
# Connect to the database
cnx = mysql.connector.connect(
    host="192.168.56.103",
#    host="10.94.255.163",
    user="perepi",
    password="pastanaga",
    database="eleccions"
)
cursor = cnx.cursor()

# Open the file
with open("04021911.DAT", "r") as file:
    # Read each line of the file
    for line in file:
        # Strip leading and trailing whitespace from the line
        data = line.strip()
        # Extract the values from the data string
        num_ordre = data[21:24]
        tipus = data[24:25]
        codi_candidatura = data[15:21]
        codi_ine_prov = data[9:11]
        nom = data[25:50].strip().replace("\"", "")
        cog1 = data[50:75].strip().replace("\"", "")
        cog2 = data[75:100].strip().replace("\"", "")
        sexe = data[100:101].strip().replace("\"", "")
        cursor.execute(f"SELECT candidatura_id FROM candidatures WHERE codi_candidatura = '{codi_candidatura}'")
        candidatura_id = cursor.fetchone()
        cursor.execute(f"SELECT provincia_id FROM provincies WHERE codi_ine = '{codi_ine_prov}'")
        provincia_id = cursor.fetchone()
        cursor.execute(f"SELECT persona_id FROM persones WHERE nom LIKE '{nom}' AND cog1 LIKE '{cog1}' AND cog2 LIKE '{cog2}' AND sexe LIKE '{sexe}'")
        persona_id = cursor.fetchone()
        query = "INSERT INTO candidats (candidatura_id, provincia_id, persona_id, num_ordre, tipus) VALUES (%s, %s, %s, %s, %s)"
        values = (candidatura_id[0], provincia_id[0], persona_id[0], num_ordre, tipus)
        cursor.execute(query, values)

# Commit the changes
cnx.commit()


# Close the cursor and connection
cursor.close()
cnx.close()
print("DONE")
```

### Insert Vots_candidatures_ca

```python
import mysql.connector
print("START")
# Connect to the database
cnx = mysql.connector.connect(
    host="192.168.56.103",
#    host="10.94.255.163",
    user="perepi",
    password="pastanaga",
    database="eleccions"
)
cursor = cnx.cursor()
# Open the file
with open("08021911.DAT", "r") as file:
    # Read each line of the file
    for line in file:
        # Strip leading and trailing whitespace from the line
        data = line.strip()
        # Extract the values from the data string
        vots = data[20:28]
        codi_ine_ca = data[9:11]
        codi_candidatura = data[14:20]
        codi_ine_prov = data[11:13]
        comunitat_aut_id= cursor.execute(f"SELECT comunitat_aut_id FROM comunitats_autonomes WHERE codi_ine = '{codi_ine_ca}'")
        comunitat_aut_id = cursor.fetchone()
        candidatura_id = cursor.execute(f"SELECT candidatura_id FROM candidatures WHERE codi_candidatura = '{codi_candidatura}'")
        candidatura_id = cursor.fetchone()
        if codi_ine_prov == "99" and codi_ine_ca != "99" :
           query = "INSERT INTO vots_candidatures_ca (comunitat_autonoma_id, candidatura_id, vots) VALUES (%s, %s, %s)"
           values = (comunitat_aut_id[0],candidatura_id[0], vots)
           cursor.execute(query, values)
        else:
            pass

# Commit the changes
cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()
print("DONE")
```

### Insert Vots_candidatures_prov

```python
import mysql.connector
print("START")
# Connect to the database
cnx = mysql.connector.connect(
    host="192.168.56.103",
#    host="10.94.255.163",
    user="perepi",
    password="pastanaga",
    database="eleccions"
)
cursor = cnx.cursor()





# Open the file
with open("08021911.DAT", "r") as file:
    # Read each line of the file
    for line in file:
        # Strip leading and trailing whitespace from the line
        data = line.strip()
        # Extract the values from the data string
        vots = data[20:28].replace("\"", "'")
        codi_ine_pro = data[11:13].replace("\"", "'")
        codi_candidatura = data[14:20].replace("\"", "'")
        candidats_obtinguts = data[28:33].replace("\"", "'") 
        provincia_id = cursor.execute(f"SELECT provincia_id FROM provincies WHERE codi_ine = '{codi_ine_pro}'")# Select
        provincia_id = cursor.fetchone()
        candidatura_id = cursor.execute(f"SELECT candidatura_id FROM candidatures WHERE codi_candidatura = '{codi_candidatura}'")# Select
        candidatura_id = cursor.fetchone()
        if codi_ine_pro != "99": 
            query = "INSERT INTO vots_candidatures_prov (provincia_id, candidatura_id, vots, candidats_obtinguts) VALUES (%s, %s, %s, %s)"
            values = (provincia_id[0], candidatura_id[0], vots, candidats_obtinguts)
            cursor.execute(query, values)
        else:
            pass

# Commit the changes
cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()
print("DONE")
```

### Insert Vots_candidatures_mun

```python
import mysql.connector

print("START")

# Connect to the database
cnx = mysql.connector.connect(
    host="192.168.56.103",
    user="perepi",
    password="pastanaga",
    database="eleccions"
)
cursor = cnx.cursor()
dubl_dict= {}
# Open the file
with open("06021911.DAT", "r") as file:
    # Read each line of the file
    for line in file:
        # Strip leading and trailing whitespace from the line
        data = line.strip()
        # Extract the values from the data string
        vots = data[22:30].replace("\"", "'")
        codi_ine_mun = data[11:14].replace("\"", "'")
        codi_candidatura = data[16:22].replace("\"", "'")
        candidats_obtinguts = data[28:33].replace("\"", "'")
        any = data[2:6]
        mes = data[6:8]
        eleccio_id = cursor.execute(f"SELECT eleccio_id FROM eleccions WHERE any = '{any}' AND mes = '{mes}'")
        eleccio_id = cursor.fetchone()
        cursor.nextset()
        municipi_id = cursor.execute(f"SELECT municipi_id FROM municipis WHERE codi_ine = '{codi_ine_mun}'")
        municipi_id = cursor.fetchone()
        cursor.nextset()
        candidatura_id = cursor.execute(f"SELECT candidatura_id FROM candidatures WHERE codi_candidatura = '{codi_candidatura}' and eleccio_id = '{eleccio_id[0]}'")
        candidatura_id = cursor.fetchone()
        cursor.nextset()
        key_form = f"{eleccio_id[0]}{municipi_id[0]}{candidatura_id[0]}"
# Add the vots to the corresponding key in the dubl_dict dictionary
        key_form = f"{eleccio_id[0]}{municipi_id[0]}{candidatura_id[0]}"
        if key_form in dubl_dict:
            dubl_dict[key_form] += int(vots)
            query = "UPDATE vots_candidatures_mun SET vots = %s WHERE eleccio_id = %s AND municipi_id = %s AND candidatura_id = %s"
            values = (dubl_dict[key_form], eleccio_id[0], municipi_id[0], candidatura_id[0])
            cursor.execute(query, values)
        else:
            dubl_dict[key_form] = int(vots)
            query = "INSERT INTO vots_candidatures_mun (eleccio_id, municipi_id, candidatura_id, vots) VALUES (%s, %s, %s, %s)"
            values = (eleccio_id[0], municipi_id[0], candidatura_id[0], vots)
            cursor.execute(query, values)
        

# Commit the changes
cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()
print("DONE")

```

# APARTAT 2

## CONSULTES SIMPLES

1.  Volem saber els noms dels municipis que començin per A:

        SELECT nom
        FROM municipis
        WHERE nom RLIKE 'A';

2. Volem saber el total de persones que hi han amb sexe masculi:

        SELECT sexe, COUNT() AS total
        FROM persones
        WHERE sexe='M'
        GROUP BY sexe;

3. Consulta per saber les eleccions que es varen fer abans del 2000:

        SELECT any 
        FROM eleccions
        WHERE any>2000;

4. Volem saber la suma de vots totals i agrupar-ho per provincia id:

        SELECT provincia_id, SUM(vots) as vots_totals
        FROM vots_candidatures_prov
        GROUP BY provincia_id;

5. Consultar el id i el nom de la comunitat autonoma de Andalucia:

        SELECT comunitat_aut_id,nom 
        FROM comunitats_autonomes
        WHERE nom='Andalucia';

### CONSULTES INNER JOIN

1. contar el numero de vots per provincia:
 
        SELECT pro.nom AS provincia, vot.vots AS num_vots
        FROM provincies pro 
        INNER JOIN vots_candidatures_prov vot ON pro.provincia_id = vot.provincia_id 

2.  Obtenir informacio de les tables eleccions_municipis,municipis i eleccions que no tinguin vots en blanc:

        SELECT * 
        FROM eleccions_municipis
        RIGHT JOIN municipis ON eleccions_municipis.municipi_id = municipis.municipi_id
        RIGHT JOIN eleccions ON eleccions_municipis.eleccio_id = eleccions.eleccio_id
        WHERE eleccions_municipis.vots_blanc = 0;

3. Volem separar per municipis i per provincia, quantes meses i vots emesos hi ha respectivament::

        SELECT p.nom AS nom_provincia, m.nom AS nom_municipi, em.num_meses AS meses, em.vots_emesos AS vots_emesos
        FROM provincies p
        INNER JOIN municipis m ON m.provincia_id = p.provincia_id
        INNER JOIN eleccions_municipis em ON m.municipi_id = em.municipi_id;

4. Volem saber l’id del municipi i el nom amb més de 50 vots en blanc:

        SELECT m.municipi_id, m.nom
        FROM municipis m
        LEFT JOIN eleccions_municipis e ON m.municipi_id=e.municipi_id
        WHERE e.vots_blanc > 50;

5. Quin es el nom de la candidatura i el numero de candidats obtinguts: 

        SELECT c.nom_curt, p.candidats_obtinguts
        FROM vots_candidatures_prov p
        LEFT JOIN candidatures c ON p.candidatura_id = c.candidatura_id
;

## SUBCONSULTES

1. Obté la eleccio_id, el municipi_id i el num de vots vàlids de les eleccions municipals amb més vots en blanc:
    
        SELECT eleccio_id, municipi_id, vots_valids
        FROM eleccions_municipis
        WHERE vots_blanc = (SELECT MAX(vots_blanc)
        FROM eleccions_municipis);
    
2. Visualitzar l'id de candidat i el nom del canditat més jove:
    
        SELECT c.candidat_id, p.nom
        FROM candidats c
        INNER JOIN persones p ON p.persona_id
        WHERE p.data_naixement=(SELECT MAX(data_naixement)
        FROM persones
        GROUP BY data_naixement);
    
3. Obtenir el nom de la província amb més vots:
    
        SELECT p.nom, v.vots
        FROM provincies p
        INNER JOIN vots_candidatures_prov v ON v.provincia_id=p.provincia_id
        WHERE v.vots = (SELECT MAX(vots)
        FROM vots_candidatures_prov);
    
4. Volem saber el nom de la comunitat autònoma amb major número d’escons:
    
        SELECT c.nom, p.num_escons
        FROM comunitats_autonomes
        INNER JOIN provincies p ON c.comunitat_aut_id=p.comunitat_aut_id
        WHERE v.num_escons=(SELECT MAX(num_escons)
        FROM provincies);
    
5. Obté el nom del municipi, el seu id, el numero de vots a candidatures i el total de vots emeoss del municipi que hagi tingut més vots nuls:
    
    
        SELECT m.nom, e.municipi_id, e.vots_candidatures, e.vots_emesos
        FROM eleccions_municipis e
        INNER JOIN municipis m ON e.municipi_id=m.municipi_id
        WHERE vots_nuls=(SELECT MAX(vots_nuls)
        FROM eleccions_municipis);
    

