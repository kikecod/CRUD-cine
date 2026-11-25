import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL

load_dotenv(override=True)

app = Flask(__name__)

#Conexion con la base de datos
app.config['MYSQL_HOST'] = os.environ['HOST']
app.config['MYSQL_USER'] = os.environ['USER']
app.config['MYSQL_PASSWORD'] = os.environ['PASSWORD']
app.config['MYSQL_DB'] = os.environ['DATABASE']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

#READ 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/peliculas/', methods=['GET'])
def listar():
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM peliculas"
        cursor.execute(sql)
        peliculas = cursor.fetchall()
        cursor.close()
        return jsonify(peliculas)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/peliculas/', methods=['POST'])
def crear():
    datos = request.get_json(silent=True)

    nombre = datos.get('nombre')
    genero = datos.get('genero')
    director = datos.get('director')
    duracion = datos.get('duracion')

    cursor = mysql.connection.cursor()
    sql = "INSERT INTO peliculas(nombre, genero, director, duracion) VALUES(%s, %s, %s, %s)"
    cursor.execute(sql, (nombre, genero, director, duracion))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"mensaje":"CREADO CORRECTAMENTE LA PELICUAL " }), 201

if __name__ == '__main__':
    app.run(debug=True, port=5001)

