import openai
from openai import OpenAI
import sqlite3
import mysql.connector


client = OpenAI(
    api_key="...",
    base_url="https://fridaplatform.com/v1"
)
queryLenguajeNatural=input("Que gustas consultar de la base de datos?:")
response = client.chat.completions.create(
    model="gpt",
    messages=[
        {"role": "user", "content": f"""CONTESTA SOLO CON LA QUERY QUE ME CONSIGA LO SIGUENTE, NADA DE TEXTO APARTE DEL QUERY: "{queryLenguajeNatural}" 
        
        BASE DE DATOS: 
        
        Tables in the database:

Table: rack_1
Columns: Id_producto, Producto, Cantidad, Rack_correspondiente
(10001, 'Product A', 50, 1)
(10002, 'Product B', 20, 1)
(10003, 'Product C', 30, 1)
(10004, 'Product D', 10, 1)
(10005, 'Product E', 25, 1)

Table: rack_2
Columns: Id_producto, Producto, Cantidad, Rack_correspondiente
(20001, 'Product F', 40, 2)
(20002, 'Product G', 15, 2)
(20003, 'Product H', 60, 2)
(20004, 'Product I', 35, 2)
(20005, 'Product J', 45, 2)"""},
    ],
    stream=False
)

generated_query = response.choices[0].message.content

print(generated_query)

# Establish the connection
conn = mysql.connector.connect(
    host='sanders.c3coace2uz12.us-east-2.rds.amazonaws.com',
    user='admin',
    password='SandersAdmin123.!',
    database='racks'  # Replace with your database name
)

# Create a cursor object
cursor = conn.cursor()

# Ensure that generated_query is defined before running this script
try:
    # Execute the query contained in generated_query
    cursor.execute(generated_query)

    # Fetch all rows from the query result
    rows = cursor.fetchall()
    
    # Print the column headers
    columns = [desc[0] for desc in cursor.description]
    print(f"Columns: {', '.join(columns)}")

    # Print all rows
    for row in rows:
        print(row)

except mysql.connector.Error as err:
    print(f"Error: {err}")
    print("Lo siento, no encuentro lo que me has pedido")

# Close the cursor and connection
cursor.close()
conn.close()
