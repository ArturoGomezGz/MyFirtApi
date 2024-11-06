from flask import Flask, request, jsonify
import mysql.connector
import pandas as pd
import json
import pyodbc

# API para mandar y recibir datos de 
baseDeDatos = {
    "driver" : "SQL Server",
    "server" : "DESKTOP-GI8HMHT",  # Cambia esto a tu servidor SQL
    "database" : "SemaforoInteligente",  # Cambia esto a tu base de datos
    "usuario" : "root",
    "contrasena" : "password",
}
stringConexion = f'DRIVER={{{baseDeDatos["driver"]}}};SERVER={baseDeDatos["server"]};DATABASE={baseDeDatos["database"]};Trusted_Connection=yes;'

def row_to_dict(cursor, data_row):
    columns = [column[0] for column in cursor.description]
    row_dict = dict(zip(columns, data_row))
    return row_dict

def query_to_json(cursor, query, params=()):
    # Ejecuta la consulta con parámetros
    cursor.execute(query, params)
    
    # Obtiene los nombres de las columnas
    columns = [column[0] for column in cursor.description]
    
    # Obtiene todas las filas de la consulta
    rows = cursor.fetchall()
    
    # Convierte cada fila en un diccionario con nombres de columna como claves
    result = [dict(zip(columns, row)) for row in rows]
    
    # Convierte el resultado en JSON
    json_result = json.dumps(result, indent=4)
    
    return json_result

app = Flask(__name__)

@app.route("/get-semaforo/<int:idSemaforo>")
def get_semaforo(idSemaforo):
    conexion = pyodbc.connect(stringConexion)
    cursor = conexion.cursor()
    
    # Consulta segura usando parámetros
    query = "SELECT * FROM Semaforo WHERE id = ?"
    cursor.execute(query, (idSemaforo,))
    resultado = cursor.fetchone()
    
    if resultado:
        data = row_to_dict(cursor, resultado)
        return jsonify(data), 200
    else:
        return jsonify({"error": "Semáforo no encontrado"}), 404

@app.route("/get-ciclos/<string:tipo>")
def get_ciclo(tipo):
    conexion = pyodbc.connect(stringConexion)
    cursor = conexion.cursor()
    
    if tipo not in ["d", "m"]:
        return jsonify({"error": "Tipo no válido"}), 400
    
    query = f"SELECT * FROM {tipo}Ciclo"
    json_result = query_to_json(cursor, query)
    return jsonify(json.loads(json_result)), 200


if __name__ == "__main__":
    app.run(debug=True)