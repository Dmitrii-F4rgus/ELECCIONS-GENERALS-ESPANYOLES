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
