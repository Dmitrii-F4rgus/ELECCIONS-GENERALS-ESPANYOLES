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

