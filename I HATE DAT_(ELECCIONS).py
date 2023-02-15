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
with open("02021911.DAT", "r") as file:
    # Read each line of the file
    for line in file:
        # Strip leading and trailing whitespace from the line
        data = line.strip()
        # Extract the values from the data string
        any = data[2:6]
        nom = data[0:2].replace("02", "Elecciones al Congreso de los Diputados") + any  
        mes = data[6:8]
        data = any + "-" + mes + "-" + data[12:14]
        query = "INSERT INTO eleccions (nom, data) VALUES (%s, %s)"
        values = (nom, data)
        cursor.execute(query, values)


# Commit the changes
cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()
