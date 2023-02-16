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
with open("05021911.DAT", "r") as file:
    # Read each line of the file
    for line in file:
        # Strip leading and trailing whitespace from the line
        data = line.strip()
        # Extract the values from the data string
        num_meses = data[136:141]
        cens = data[141:149]
        vots_candidatures = data[205:213]
        vots_candidatures = int(vots_candidatures)
        vots_blanc = data[189:197]
        vots_blanc = int(vots_blanc)
        vots_nuls = data[197:205]
        vots_nuls = int(vots_nuls)
        vots_emesos = vots_candidatures + vots_blanc + vots_nuls
        vots_emesos = int(vots_emesos)
        vots_valids = vots_emesos - vots_nuls
        vots_valids = int(vots_valids)
        codi_ine_mu = data[13:16]
        codi_ine_prov = data[11:13].replace("\"", "'")
        any = data[2:6]
        mes = data[6:8]
        codi_dstrc = data[16:18]
        provincia_id=cursor.execute(f"SELECT provincia_id FROM provincies WHERE codi_ine = '{codi_ine_prov}'")# Select
        provincia_id = cursor.fetchone()
        municipi_id=cursor.execute(f"SELECT municipi_id FROM municipis WHERE codi_ine = '{codi_ine_mu}' AND provincia_id = '{provincia_id[0]}' AND districte = '{codi_dstrc}'")# Select
        municipi_id = cursor.fetchone()
        eleccio_id=cursor.execute(f"SELECT eleccio_id FROM eleccions WHERE any = '{any}' AND mes = '{mes}'")# Select
        eleccio_id = cursor.fetchone()
        query = "INSERT INTO eleccions_municipis (eleccio_id, municipi_id, num_meses, cens, vots_emesos, vots_valids, vots_candidatures, vots_blanc, vots_nuls) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (eleccio_id[0], municipi_id[0], num_meses, cens, vots_emesos, vots_valids, vots_candidatures, vots_blanc, vots_nuls)
        cursor.execute(query, values)

# Commit the changes
cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()
print("DONE")
