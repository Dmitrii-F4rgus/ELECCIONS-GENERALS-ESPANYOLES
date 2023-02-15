import mysql.connector

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
