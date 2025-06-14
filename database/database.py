# database.py

import sqlite3
import os
from datetime import datetime

# Définir le chemin vers la base de données
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'users.db')


# Connexion directe à la DB 
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# Création de la table des utilisateurs
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            fullname TEXT,
            email TEXT,
            role TEXT NOT NULL DEFAULT 'Utilisateur',
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Création de la table des détections, liée à un utilisateur
def init_db_detection():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            url TEXT,
            ip_src TEXT,
            ip_dst TEXT,
            protocole TEXT,
            verdict TEXT,
            timestamp TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()

# Initialisation automatique des tables
def ensure_db_initialized():
    init_db()
    init_db_detection()

# Appel immédiat à l’importation
ensure_db_initialized()

# Insertion d’une capture liée à un utilisateur
def insert_detection(user_id, url, ip_src, ip_dst, protocole, verdict, timestamp):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO detections (user_id, url, ip_src, ip_dst, protocole, verdict, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, url, ip_src, ip_dst, protocole, verdict, timestamp))
    conn.commit()
    conn.close()

# Récupérer les captures récentes d’un utilisateur
def get_detections_for_user(user_id, limit=10):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT * FROM detections
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (user_id, limit))
    rows = cur.fetchall()
    conn.close()
    return rows

# Supprimer les captures d’un utilisateur 
def clear_detections_for_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('DELETE FROM detections WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()



