import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv(override=True)

app = Flask(__name__)

#Conexion con la base de datos
app.config['MYSQL_HOST'] = os.environ['HOST']
app.config['MYSQL_USER'] = os.environ['USER']
app.config['MYSQL_PASSWORD'] = os.environ['PASSWORD']
app.config['MYSQL_DB'] = os.environ['DATABASE']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#clave secreta para firmar los tokens de JWT
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET']

mysql = MySQL(app)
jwt = JWTManager(app)

@app.route('/registro', methods=['POST'])
def registro():
    datos = request.get_json(silent=True) or {}
    username = datos.get('username')
    password = datos.get('password')

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE username = %s", (username,))
        if cursor.fetchone():
            cursor.close()
            return jsonify({"error": "usuario existente"}),409

        sql = "INSERT INTO usuarios(username, password_hash) VALUES (%s,%s)"
        cursor.execute(sql, (username, generate_password_hash(password)))
        mysql.connection.commit()
        cursor.close()
        return jsonify({"mensjae": "usuario creado correctamente"})
    except Exception as e:
        return jsonify({"error":str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    datos = request.get_json(silent=True) or {}
    username = datos.get('username')
    password = datos.get('password')

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT username, password_hash FROM usuarios WHERE username = %s", (username.strip(), ))
        usuario = cursor.fetchone()
        cursor.close()
    except Exception as e:
        return jsonify({"error":str(e)}), 500

    if usuario and check_password_hash(usuario['password_hash'], password):
        token = create_access_token(identity=usuario['username'])
        return jsonify(access_token=token),200

    return jsonify({"error": "credenciales incorrectas"}),401


#READ 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form')
def form():
    return render_template('form.html')

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
@jwt_required()
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

@app.route('/api/peliculas/<int:id>', methods=['PUT'])
def editar(id):
    datos = request.get_json(silent=True)

    nombre = datos.get('nombre')
    genero = datos.get('genero')
    director = datos.get('director')
    duracion = datos.get('duracion')

    cursor = mysql.connection.cursor()
    sql = "UPDATE peliculas SET nombre = %s, genero = %s, director = %s, duracion = %s WHERE id = %s"
    cursor.execute(sql, (nombre, genero, director, duracion, id))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"mensaje":"pelicula actualizada"})


if __name__ == '__main__':
    app.run(debug=True, port=5001)

