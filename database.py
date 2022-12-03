#-------------------- Modulos --------------------
import mysql.connector as db;
import json;

#-------------------- Obtener las claves --------------------
with open('config.json') as file:
    data = json.load(file);
    host = data['host'];
    user = data['user'];
    password = data['password'];
    database = data['database'];

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
        

