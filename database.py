#-------------------- Modulos --------------------
from datetime import datetime
import mysql.connector as db;
import json;

#-------------------- Obtener las claves --------------------
with open('config.json') as file:
    data = json.load(file);
    host = data['host'];
    user = data['user'];
    password = data['password'];
    database = data['database'];
horaEntrada = "08:00:00";

#Registro de un nuevo usuario en la base de datos
def registrar_usuario( nombre, codigo ):
    id = 0
    insertado = 0
    try:
        conexion = db.connect(host=host, user=user, password=password, database=database);
        cursor = conexion.cursor();
        cursor.execute(f"INSERT INTO usuarios (nombre, foto) VALUES ('{nombre}', '{codigo}')");
        conexion.commit(); 
        conexion.close();
        insertado = cursor.rowcount; # 1 si se inserto correctamente
        id = cursor.lastrowid; # Obtener el id del ultimo registro
    except db.Error as e:
        print(e);
    finally: 
        if conexion.is_connected():
            conexion.close();
            cursor.close();
    return {"id": id, "insertado": insertado};
        
#Obtención de los nombres de los usuarios de la BD
def obtener_usuarios():
    usuarios = [];
    try:
        conexion = db.connect(host=host, user=user, password=password, database=database);
        cursor = conexion.cursor();
        cursor.execute("SELECT nombre FROM usuarios");
        usuarios = cursor.fetchall();
        conexion.close();
    except db.Error as e:
        print(e);
    finally: 
        if conexion.is_connected():
            conexion.close();
            cursor.close();
    return usuarios;

#Obtención del codigo de un usuario
def obtener_usuario( usuario ):
    codigo = "";
    try:
        conexion = db.connect(host=host, user=user, password=password, database=database);
        cursor = conexion.cursor();
        cursor.execute(f"SELECT foto FROM usuarios WHERE nombre = '{usuario}'");
        codigo = cursor.fetchone();
        conexion.close();
    except db.Error as e:
        print(e);
    finally: 
        if conexion.is_connected():
            conexion.close();
            cursor.close();
    return codigo[0];
    
#Agregar a la base de datos la hora de entrada de un usuario
def agregar_asistencia( usuario ):
    insertado = 0
    estado = ""
    try:
        #Checar si no tiene retardo 
        horaActual = datetime.now().strftime("%H:%M:%S");
        print(horaActual);
        if horaActual > horaEntrada:
            estado = "Retardo";
        else:
            estado = "Correcto";
        conexion = db.connect(host=host, user=user, password=password, database=database);
        cursor = conexion.cursor();
        #Gurdar en la tabla los campos, nombre, hora, fecha y estado
        #Obtener la hora y fecha actual python
        cursor.execute(f"INSERT INTO asistencias (nombre, hora, fecha, estado) VALUES ('{usuario}', '{horaActual}', '{datetime.now().strftime('%Y-%m-%d')}', '{estado}')");
        conexion.commit();
        conexion.close();
        insertado = 1;
    except db.Error as e:
        print(e);
    finally: 
        if conexion.is_connected():
            conexion.close();
            cursor.close();
    return insertado;