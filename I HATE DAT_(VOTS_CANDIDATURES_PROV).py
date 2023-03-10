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
