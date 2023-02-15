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
contador = 0
# Open the file
with open("04021911.DAT", "r") as file:
    # Read each line of the file
    for line in file:
        # Strip leading and trailing whitespace from the line
        data = line.strip()
        # Extract the values from the data string
        persona_id = contador=contador+1
        nom = data[25:50].strip().replace("\"", "'")
        cog1 = data[50:75].strip().replace("\"", "'")
        cog2 = data[75:100].strip().replace("\"", "'")
        sexe = data[100:101].replace("\"", "'")
        DAY_naixement = data[101:103].replace("\"", "'")
        MES_naixement = data[103:105].replace("\"", "'")
        ANO_naixement = data[105:109].replace("\"", "'")
        #Fer que data_naixement sigui un valor com a data
        data_naixement = ANO_naixement + "-" + MES_naixement + "-" + DAY_naixement 
        dni = data[109:119].replace("\"", "'")
        query = "INSERT INTO persones (persona_id, nom, cog1, cog2, sexe, data_naixement, dni) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (persona_id, nom, cog1, cog2, sexe, data_naixement, dni)
        cursor.execute(query, values)

# Commit the changes
cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()
