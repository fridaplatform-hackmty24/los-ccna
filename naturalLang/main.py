#standard libraries
import os
import io
import re
import subprocess

"""
installs:
pip install google-cloud-speech
pip install openai
"""

#Third-party libraries
import pygame
import sqlite3
import mysql.connector
from gtts import gTTS
import sounddevice as sd
import scipy.io.wavfile as wav
from google.oauth2 import service_account
from google.cloud import speech
import openai
from openai import OpenAI

#OPENAI credentials
openai_client = OpenAI(
    api_key="...",
    base_url="https://fridaplatform.com/v1"
)

#GOOGLE credentials
client_file='sonorous-reach-435702-r9-dc6c717cd4fa.json'
credentials= service_account.Credentials.from_service_account_file(client_file)
client=speech.SpeechClient(credentials=credentials)

#record voice for 5 seconds
def record_audio(filename, duration, samplerate=44100):
    print(f"Recording for {duration} seconds...")
    # Record audio
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    # Save to WAV file
    wav.write(filename, samplerate, recording)
    print(f"Recording saved to {filename}")
    return filename

#parse the google response to get transcript
def parse_results(response):
    # Extract transcript from the response object
    transcript = None
    if hasattr(response, 'results') and len(response.results) > 0:
        alternatives = response.results[0].alternatives
        if len(alternatives) > 0:
            transcript = alternatives[0].transcript
    return transcript

def perform_search():
    #record audio to output.wav file
    filename = record_audio("output.wav", duration=5)
    audio_file='output.wav'

    #Recognize speech and generate a transcript variable, transcript holds the actual
    #thing the user said, since TextResponse is a pseudo-json file lol
    with io.open(audio_file,'rb') as f:
        content=f.read()
        audio=speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code='es-MX'
    )
    TextResponse=client.recognize(config=config,audio=audio)

    #this is our precious natural language query from the user
    transcript=parse_results(TextResponse)
    print(transcript)

    #we now communicate the natural language query with the frida api to get the response we want
    response = openai_client.chat.completions.create(
        model="gpt",
        messages=[
            {"role": "user", "content": f"""CONTESTA SOLO CON LA QUERY QUE ME CONSIGA LO SIGUENTE, NADA DE TEXTO APARTE DEL QUERY: "{transcript}" 
            
            BASE DE DATOS:
        
            Cada una de las tablas consiste en las columnas:Id_producto, Producto, Cantidad, Rack_correspondiente
            La primera tabla se llama rack_1, con columnas: Id_producto, Producto, Cantidad, Rack_correspondiente
            La segunda tabla se llama rack_2, con columnas: Id_producto, Producto, Cantidad, Rack_correspondiente
            La tercera tabla se llama rack_3, con columnas: Id_producto, Producto, Cantidad, Rack_correspondiente
            La cuarta tabla se llama rack_4, con columnas: Id_producto, Producto, Cantidad, Rack_correspondiente
            La quinta tabla se llama rack_5, con columnas: Id_producto, Producto, Cantidad, Rack_correspondiente

            Consulta todas estas tablas para satisfacer el query, no tienes permiso de modificar nada.
    """},
        ],
        stream=False
    )
    #this is frida's response, which should be just the query, else, we will get syntax errors or similar
    generated_query = response.choices[0].message.content
    print(generated_query)

    #We now establish a connection with the sql database
    conn = mysql.connector.connect(
        host='sanders.c3coace2uz12.us-east-2.rds.amazonaws.com',
        user='admin',
        password='SandersAdmin123.!',
        database='racks'
    )

    #we create  a cursor object
    cursor = conn.cursor()

    #we make sure the query is defined before running it
    try:
        #we execute the query
        cursor.execute(generated_query)

        #get all the rows from the query result
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
        #print("Query Results:")
        #print(results)

        #We refubrish the response into something any common non-programmer could understand
        response1 = openai_client.chat.completions.create(
        model="gpt",
        messages=[
            {"role": "user", "content": f""" pregunta:{transcript}, queryderivado:{generated_query}, resultado de la base de datos: {results}
            tomando en cuenta estos, di cual es el resultado de la busqueda brevemente y mencionale en que rack esta el producto que quiere en caso de que aplique, siguiendo el formato Rack (numero de rack).
            
            """},
        ],
        stream=False
        )

        softenedResponse = response1.choices[0].message.content
        print("softenedresponse:",softenedResponse)
        pattern = r'Rack (\d+)'
        match = re.search(pattern, softenedResponse)
        if match:
            rack_number = int(match.group(1))
            print(f'The rack number is: {rack_number}')
            language="es"
            gtts_object=gTTS(text=softenedResponse, lang=language, slow=False)
            gtts_object.save("gtts.mp3")

            pygame.mixer.init()
            pygame.mixer.music.load('gtts.mp3')
            pygame.mixer.music.play()

            # Keep the program running until the sound finishes
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            return rack_number
            
        else:
            print('Rack number not found.')
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        softenedResponse="Lo siento, no encuentro lo que me has pedido, puedes intentar de nuevo"

    #Close the cursor and connection
    cursor.close()
    conn.close()

    #we now convert that response to TTS so the user can hear the response to the query in a language they can understand
    language="es"
    gtts_object=gTTS(text=softenedResponse, lang=language, slow=False)
    gtts_object.save("gtts.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load('gtts.mp3')
    pygame.mixer.music.play()

    # Keep the program running until the sound finishes
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def main():
    while True:
        rack_number = perform_search()
        if rack_number is not None:
            print(f"Rack number returned: {rack_number}")
            
            break
        else:
            #time.sleep(5)
            print("Retrying search...")

if __name__ == "__main__":
    main()
