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
