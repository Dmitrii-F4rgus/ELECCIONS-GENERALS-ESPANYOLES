import mysql.connector

# Connect to the database
cnx = mysql.connector.connect(
    host="192.168.56.103",
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
        vots = data[20:28].replace("\"","'")
        codi_ine_comu = data[9:11].replace("\"","'")
        codi_candidaturas = data[14:20].replace("\"","'")
        IHATEDATSYKA= cursor.execute(f"SELECT comunitat_aut_id FROM comunitats_autonomes WHERE codi_ine = '{codi_ine_comu}'")
        IHATEDATSYKA = cursor.fetchone()
        print("CA",IHATEDATSYKA)
        IHATEDATSYKA1 = cursor.execute(f"SELECT candidatura_id FROM candidatures WHERE codi_candidatura = '{codi_candidaturas}'")
        IHATEDATSYKA1 = cursor.fetchone()
        print("CAN",IHATEDATSYKA1)
        

        if line[11:13] == "99" and codi_ine_comu != "99" :

           query = "INSERT INTO vots_candidatures_ca (comunitat_autonoma_id, candidatura_id, vots) VALUES (%s, %s, %s)"
           values = (IHATEDATSYKA[0],IHATEDATSYKA1[0], vots)
           cursor.execute(query, values)
        else:
            pass

# Commit the changes
cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()
