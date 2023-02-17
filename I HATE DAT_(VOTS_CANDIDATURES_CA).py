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
