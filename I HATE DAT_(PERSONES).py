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
contador = 0
# Open the file
full_name_list= ["START"]
with open("04021911.DAT", "r") as file:
    # Read each line of the file
    for line in file:
        # Strip leading and trailing whitespace from the line
        data = line.strip()
        # Extract the values from the data string
        persona_id = contador=contador+1
        nom = data[25:50].strip().replace("\"", "")
        cog1 = data[50:75].strip().replace("\"", "")
        cog2 = data[75:100].strip().replace("\"", "")
        sexe = data[100:101].replace("\"", "'")
        DAY_naixement = data[101:103]
        MES_naixement = data[103:105]
        ANO_naixement = data[105:109]
        data_naixement = ANO_naixement + "-" + MES_naixement + "-" + DAY_naixement 
        dni = data[109:119].strip()
        full_name = f"{nom} {cog1} {cog2}"
        full_name_list.append(full_name)
        if data_naixement == "0000-00-00" and full_name_list.count(full_name) < 2:
                query = "INSERT INTO persones (persona_id, nom, cog1, cog2, sexe, data_naixement, dni) VALUES (%s, %s, %s, %s, %s, %s, %s)"        
                values = (persona_id, nom, cog1, cog2, sexe, None, dni)
                cursor.execute(query, values)
        elif data_naixement != "0000-00-00" and full_name_list.count(full_name) < 2:
                query = "INSERT INTO persones (persona_id, nom, cog1, cog2, sexe, data_naixement, dni) VALUES (%s, %s, %s, %s, %s, %s, %s)"        
                values = (persona_id, nom, cog1, cog2, sexe, data_naixement, dni)
                cursor.execute(query, values)
        else:
                pass
                
# Commit the changes
cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()
print("DONE")
