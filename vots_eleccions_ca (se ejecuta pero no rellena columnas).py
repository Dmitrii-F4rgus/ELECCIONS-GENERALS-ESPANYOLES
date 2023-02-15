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
        comunitat_autonoma_id = cursor.execute(f"SELECT comunitat_aut_id FROM comunitats_autonomes WHERE codi_ine = '{line[9:11]}'")
        comunitat_autonoma_id = cursor.fetchone()                                       
        candidatura_id = cursor.execute(f"SELECT candidatura_id FROM candidatures WHERE codi_candidatura = '{line[15:21]}'")
        candidatura_id = cursor.fetchone()
        vots = cursor.execute(f"SELECT candidatura_id FROM candidatures WHERE candidatura_id = '{line[20:28]}'")
        vots = cursor.fetchone()
        if codi_ine != "99" and codi_ine_prov == "99":
                query = "INSERT INTO comunitats_autonomes (comunitat_autonoma_id, candidatura_id, vots) VALUES (%s, %s)"
                values = (comunitat_autonoma_id, candidatura_id, vots)
                cursor.execute(query, values)
        else:
            pass


# Commit the changes
cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()
