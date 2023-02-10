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
