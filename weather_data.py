import requests
import pandas as pd 
from datetime import datetime
import psycopg2
import schedule
import time

# Définir votre clé API pour OpenWeatherMap et la liste des villes
API_KEY = 'b59ef2a1aa9da64e6ffcbe63952b97b8'
cities = ['Dakar', 'Thies']

def get_weather_data(city):
    """
    Fonction pour obtenir les donnees meteorologiques d'une ville spécifique.
    Args:
        city (str): Le nom de la ville.
    Returns:
        dict: Un dictionnaire contenant les donnees meteorologiques.
    """
    # Construire l'URL pour accéder à l'API OpenWeatherMap
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    
    # Faire une requête HTTP GET à l'API
    response = requests.get(url)
    
    # Convertir la réponse JSON en dictionnaire Python
    data = response.json()
    
    # Retourner un dictionnaire avec les donnees meteorologiques
    return {
        'city': data['name'],
        'temperature': data['main']['temp'],
        'description': data['weather'][0]['description'],
        'pressure': data['main']['pressure'],
        'humidity': data['main']['humidity'],
        'timestamp': datetime.now()  # Ajouter un horodatage pour les donnees
    }

def store_weather_data(data):
    """
    Fonction pour stocker les donnees meteorologiques dans la base de donnees.
    Args:
        data (DataFrame): Les donnees meteorologiques sous forme de DataFrame.
    """
    # Connexion à la base de donnees 
    conn = psycopg2.connect("dbname=weather_db user=postgres password=postgres")
    cur = conn.cursor()
    
    # Insérer chaque ligne de donnees dans la table weather_data
    for index, row in data.iterrows():
        cur.execute("""
            INSERT INTO weather_data (city, temperature, description, pressure, humidity, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (row['city'], 
              row['temperature'], 
              row['description'], 
              row['pressure'], 
              row['humidity'], 
              row['timestamp']))
    
    # Valider et fermeture de la session
    conn.commit()
    cur.close()
    conn.close()

def create_database_and_table(): 
    """
    Fonction pour creer la base de donnees et la table si elles n'existent pas.
    """
    # Connexion à la base de donnees par défaut pour creer une nouvelle base de donnees
    conn = psycopg2.connect("dbname=weather_db user=postgres password=postgres") 
    conn.autocommit = True 
    cur = conn.cursor()  
    
    # creer la base de donnees s'il n'existe pas
    try: 
        cur.execute("CREATE DATABASE weather_db") 
    except psycopg2.errors.DuplicateDatabase: 
        pass 
    conn.close() 
    
    # Connexion à la nouvelle base de donnees pour creer la table
    conn = psycopg2.connect("dbname=weather_db user=postgres password=postgres") 
    cur = conn.cursor() 
    
    # creer la table weather_data si elle n'existe pas
    cur.execute(""" 
                CREATE TABLE IF NOT EXISTS weather_data ( 
                id SERIAL PRIMARY KEY, 
                city VARCHAR(50), 
                temperature FLOAT, 
                description VARCHAR(100), 
                pressure INTEGER, 
                humidity INTEGER, 
                timestamp TIMESTAMP 
                ) 
                """) 
    conn.commit() 
    cur.close() 
    conn.close()


def job():
    """
    Fonction pour scraper et stocker les donnees meteorologiques.
    """
    # Obtenir les donnees meteorologiques pour chaque ville
    weather_data = [get_weather_data(city) for city in cities]
    
    # Convertir les donnees en DataFrame
    df = pd.DataFrame(weather_data)
    
    # Stocker les donnees dans la base de donnees
    store_weather_data(df)
    
    # Afficher un message de confirmation avec l'horodatage actuel
    print(f"Data scraped and stored at {datetime.now()}")


def show_weather_data(): 
    """
    Fonction pour afficher les données météorologiques stockées dans la base de données PostgreSQL.
    """
    # Connexion à la base de données PostgreSQL
    conn = psycopg2.connect("dbname=weather_db user=postgres password=postgres") 
    cur = conn.cursor() 
    
    # Exécuter une requête pour récupérer toutes les données de la table weather_data
    cur.execute("SELECT * FROM weather_data") 
    rows = cur.fetchall() 
    
    # Afficher chaque ligne de données
    for row in rows: 
        print(row) 
    
    cur.close()
    conn.close()

""" 
creer la base de donnees et la table
NB : il faut decomenter la ligne 143 si c'est la premiere fois que vous executez ce code
"""
# create_database_and_table()

# Exécuter la tâche pour scraper les donnees immédiatement
job()

show_weather_data()
# Planifier la tâche pour exécuter quotidiennement à 08:00
schedule.every().day.at("08:00").do(job)

# Boucle pour vérifier les tâches planifiées et les exécuter au bon moment
while True:
    schedule.run_pending()
    time.sleep(1)