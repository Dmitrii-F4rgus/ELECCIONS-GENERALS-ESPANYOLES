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
with open("03021911.DAT", "r") as file:
    # Read each line of the file
    for line in file:
        # Strip leading and trailing whitespace from the line
        data = line.strip()
        # Extract the values from the data string
        codi_candidatura = data[8:14]
        nom_curt = data[14:64].strip().replace("\"", "'")
        nom_llarg = data[64:214].strip().replace("\"", "'")
        codi_acumulacio_provincia = data[214:220]
        codi_acumulacio_ca = data[220:226]
        codi_acumulario_nacional = data[226:232]
        query = "INSERT INTO candidatures (codi_candidatura, nom_curt, nom_llarg, codi_acumulacio_provincia, codi_acumulacio_ca, codi_acumulario_nacional) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (codi_candidatura, nom_curt, nom_llarg, codi_acumulacio_provincia, codi_acumulacio_ca, codi_acumulario_nacional)
        cursor.execute(query, values)

# Commit the changes
cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()
print("DONE")
