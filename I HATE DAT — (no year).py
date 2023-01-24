# Open the file
with open('03021911.DAT', 'r') as file:
    # Read each line of the file
    for line in file:
        # Strip leading and trailing whitespace from the line
        data = line.strip()
        # Extract the values from the data string
        eleccio_type = data[0:2]
        codi_candidatura = data[8:14]
        nom_curt = data[14:64].strip()
        nom_llarg = data[64:214].strip()
        codi_acumulacio_provincia = data[214:220]
        codi_acumulacio_ca = data[220:226]
        codi_acumulario_nacional = data[226:232]

        # Create the query
        query = f"INSERT INTO candidaturas (eleccio_type, codi_candidatura, nom_curt, nom_llarg, codi_acumulacio_provincia, codi_acumulacio_ca, codi_acumulario_nacional) VALUES ('{eleccio_type}', '{codi_candidatura}', '{nom_curt}', '{nom_llarg}', '{codi_acumulacio_provincia}', '{codi_acumulacio_ca}', '{codi_acumulario_nacional}');"
        # Print the query
        print(query)
