import mysql.connector

print("START")

# Connect to the database
cnx = mysql.connector.connect(
    host="192.168.56.103",
    user="perepi",
    password="pastanaga",
    database="eleccions"
)
cursor = cnx.cursor()
dubl_dict= {}
# Open the file
with open("06021911.DAT", "r") as file:
    # Read each line of the file
    for line in file:
        # Strip leading and trailing whitespace from the line
        data = line.strip()
        # Extract the values from the data string
        vots = data[22:30].replace("\"", "'")
        codi_ine_mun = data[11:14].replace("\"", "'")
        codi_candidatura = data[16:22].replace("\"", "'")
        candidats_obtinguts = data[28:33].replace("\"", "'")
        any = data[2:6]
        mes = data[6:8]
        eleccio_id = cursor.execute(f"SELECT eleccio_id FROM eleccions WHERE any = '{any}' AND mes = '{mes}'")
        eleccio_id = cursor.fetchone()
        cursor.nextset()
        municipi_id = cursor.execute(f"SELECT municipi_id FROM municipis WHERE codi_ine = '{codi_ine_mun}'")
        municipi_id = cursor.fetchone()
        cursor.nextset()
        candidatura_id = cursor.execute(f"SELECT candidatura_id FROM candidatures WHERE codi_candidatura = '{codi_candidatura}' and eleccio_id = '{eleccio_id[0]}'")
        candidatura_id = cursor.fetchone()
        cursor.nextset()
        key_form = f"{eleccio_id[0]}{municipi_id[0]}{candidatura_id[0]}"
# Add the vots to the corresponding key in the dubl_dict dictionary
        key_form = f"{eleccio_id[0]}{municipi_id[0]}{candidatura_id[0]}"
        if key_form in dubl_dict:
            dubl_dict[key_form] += int(vots)
            query = "UPDATE vots_candidatures_mun SET vots = %s WHERE eleccio_id = %s AND municipi_id = %s AND candidatura_id = %s"
            values = (dubl_dict[key_form], eleccio_id[0], municipi_id[0], candidatura_id[0])
            cursor.execute(query, values)
        else:
            dubl_dict[key_form] = int(vots)
            query = "INSERT INTO vots_candidatures_mun (eleccio_id, municipi_id, candidatura_id, vots) VALUES (%s, %s, %s, %s)"
            values = (eleccio_id[0], municipi_id[0], candidatura_id[0], vots)
            cursor.execute(query, values)
        

# Commit the changes
cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()
print("DONE")

