import openai
from openai import OpenAI
import pygame
import os
import sqlite3
import mysql.connector
from gtts import gTTS


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
        La primera tabla se llama rack_1, con columnas: Id_producto, Producto, Cantidad, Rack_correspondiente
        La segunda tabla se llama rack_2, con columnas: Id_producto, Producto, Cantidad, Rack_correspondiente

        Consulta estas tablas para satisfacer el query
"""},
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

    # Initialize the results string with column names
    results = f"Columns: {', '.join(columns)}\n"

    # Add data rows to the results string
    for row in rows:
        print(row)
        results += ', '.join(str(value) for value in row) + "\n"

    # Print results for debugging
    print("Query Results:")
    print(results)

except mysql.connector.Error as err:
    print(f"Error: {err}")
    results="Lo siento, no encuentro lo que me has pedido, puedes intentar de nuevo"

#Close the cursor and connection
cursor.close()
conn.close()

#this is the tts part, which will take the query result, format it to natural lang and say it

language="es"
gtts_object=gTTS(text=results, lang=language, slow=False)
gtts_object.save("gtts.mp3")

pygame.mixer.init()
pygame.mixer.music.load('gtts.mp3')
pygame.mixer.music.play()

# Keep the program running until the sound finishes
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

