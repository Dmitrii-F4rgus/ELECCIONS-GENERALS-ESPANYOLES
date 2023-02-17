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
cursor.execute(" DROP DATABASE eleccions;")
cnx.commit()

# Close the cursor and connection
cursor.close()
cnx.close()
print("DONE")
