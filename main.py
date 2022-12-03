#-------------------- Modulos --------------------
import cv2;
import face_recognition as fr;
import numpy as np;
from tkinter import *;
from tkinter import messagebox as ms;
import os;
import threading as hilo;
import database as db;

#-------------------- Configuraciones generales --------------------
path = "C:/Users/arman/Desktop/IA/";

txt_title = "Sistema de reconocimiento facial";
txt_login = "Inciar sesión";
txt_register = "Registrarse";
txt_exit = "Salir";
color_white = "#f4f5f4";
color_black = "#000000";
color_red_btn = "#ca0e01";
color_red_btn_a = "#960d03";
color_primario = "#0a4055";
color_secundario = "#039ca7";
color_terciario = "#2b2726";
color_btn = "#274862";
font_label = "Helvetica";
size_screen = "500x500"

#Crear la ventana principal
root = Tk();
root.geometry( size_screen );
root.title( txt_title );

#-------------------- Funciones --------------------
#Función para separar los widgets
def getEnter(screen):
    ''' Set an enter inside the screen '''
    Label(screen, text="", bg=color_secundario).pack()

#Validar el campo de usuario
def comprobarCredenciales( usuario ):
    # validar que el campo no este vacio y sean puras letras
    usuario = usuario.get();
    if not usuario.isalpha():
        ms.showwarning("Error", "Debe ingresar un nombre valido")
        ventana_1.deiconify();
        return True
    return False;

#Función que configura las ventanas nuevas
def configurar_ventana( ventana, texto, titulo ):    
    ventana.geometry( size_screen );
    ventana.title( titulo );
    ventana.configure(bg=color_secundario);
    Label( ventana, text = texto, bg=color_primario, font = (font_label, 20), pady="20", fg = color_white, width=500 ).pack();

#Función para diseñar la ventana de registro
def credenciales_ventana_registro( ventana, var ):
    getEnter( ventana );
    Label(ventana, text="Usuario:", fg=color_black, font = (font_label, 17), bg=color_secundario, pady="5").pack()
    entry = Entry(ventana, textvariable=var, justify=CENTER, font=(font_label, 15))
    entry.focus_force()
    entry.pack(side=TOP, ipadx=35, ipady=8)
    getEnter( ventana );
    getEnter( ventana );

    #Boton para capturar rostro
    Button(ventana, text="Capturar rostro", fg=color_white, bg=color_terciario, activebackground=color_black, borderwidth=0, font=(font_label, 14), height="2", width="35", command=registrar_imagen).pack()
    getEnter( ventana );
    getEnter( ventana );
    getEnter( ventana );
    getEnter( ventana );
    getEnter( ventana );
    getEnter( ventana );
    #Boton para salir
    Button( ventana, text="SALIR", fg=color_white, bg=color_red_btn, activebackground=color_red_btn_a, borderwidth=0, font=(font_label, 14), pady="2", width="13", command=ventana.destroy ).pack()
    return entry;

#Función para diseñar la ventana de asistencia
def credenciales_ventana_asistencia( ventana, var ):
    getEnter( ventana );    
    #Obtener los usuarios de la base de datos
    usuarios = db.obtener_usuarios();
    #Mostrarlos en un listbox
    global listbox;
    listbox = Listbox(ventana, width=20, height=10, font=(font_label, 15), selectmode=SINGLE, justify=CENTER, bg=color_white, fg=color_black);
    listbox.pack();
    getEnter( ventana );
    i = 0
    #Agregar los usuarios al listbox
    for nombre in usuarios:
        listbox.insert(i, nombre[0]);
        i += 1;
    #Boton para tomar asistencia
    Button(ventana, text="Comparar rostro", fg=color_white, bg=color_terciario, activebackground=color_black, borderwidth=0, font=(font_label, 14), height="2", width="35", command=obtener_datos).pack()
    getEnter( ventana );
    #Boton para salir
    Button( ventana, text="SALIR", fg=color_white, bg=color_red_btn, activebackground=color_red_btn_a, borderwidth=0, font=(font_label, 14), pady="2", width="14", command=ventana.destroy ).pack()
    return ""

#Función para crear la funcionalidad de la ventana de registro
def registro():
    global usuario_1
    global usuario_tf_1
    global ventana_1
    
    ventana_1 = Toplevel(root); # Crear ventana
    usuario_1 = StringVar(); # Variable para el nombre de usuario
    
    configurar_ventana( ventana_1, "Ingrese sus datos" ,txt_register );
    usuario_tf_1 = credenciales_ventana_registro( ventana_1, usuario_1);


#Función que ayuda a capturar la imagen
def registrar_imagen():
    if comprobarCredenciales(usuario_1):
       return 0; 

    bandera = True;
    cap =  cv2.VideoCapture(0, cv2.CAP_DSHOW); # Iniciar camara
    bandera = cap.isOpened(); # Verificar si la camara esta abierta
    # Agregar el nombre con 3 letras aleatorios
    nombre_imagen = usuario_1.get().upper() +"_"+ str(np.random.randint(100, 999)) + ".jpg";
    url_imagen = path + nombre_imagen;  
    
    while bandera:
        ret, frame = cap.read(); # Leer imagen
        cv2.putText(frame, "Presiona 's' para capturar o 'ESC' para salir", (10, 20), 4, 0.7, (255, 255, 255), 1);
        k = cv2.waitKey(1);
        # Si se presiona la tecla "q" se toma la foto
        if k & 0xFF == ord('s'): 
            cv2.imwrite(url_imagen, frame); # Guardar imagen
            break;
        # Si se presiona la tecla "ESC" se cierra la ventana
        if k & 0xFF == 27: 
            bandera = False;
            break;
        cv2.imshow("Registro", frame); # Mostrar imagen
    
    cap.release(); # Liberar camara
    cv2.destroyAllWindows(); # Cerrar ventana
    # Si se tomo la foto puede continuar
    if bandera:
        procesar_imagen(url_imagen, nombre_imagen);

#Función que codifica la imagen y recibe la respuesta de la base de datos
def procesar_imagen(url_imagen, nombre):
    imagen = cv2.imread(nombre); # Leer imagen
    nombre = nombre.replace(".jpg", ""); # Quitar la extensión
    if(fr.face_locations(imagen) == []):
        ventana_1.destroy();
        ms.showerror("Error", "No se detecto un rostro en la imagen");
        os.remove(url_imagen); # Eliminar imagen
        return 0;
    imagen_loc = fr.face_locations(imagen)[0]; # Obtener ubicacion de la cara
    imagen_encode = fr.face_encodings(imagen, known_face_locations=[imagen_loc]); # Obtener codificacion de la cara
    #convertir imagen_encode en cadena
    imagen_encode = str(imagen_encode[0]);
    resultado = db.registrar_usuario(nombre, imagen_encode);

    if resultado["insertado"]:
        ms.showinfo("Registro", "Registro exitoso! \nSu usuario es: " + nombre);
        ventana_1.destroy();
    else:
        ms.showerror("Registro", "Error al registrar")
        ventana_1.destroy();
    os.remove(url_imagen); # Eliminar imagen

#Función para crear la funcionalidad de la ventana de asistencia
def acceder():
    global usuario_2
    global usuario_tf_2
    global ventana_2

    ventana_2 = Toplevel(root); # Crear ventana
    usuario_2 = StringVar(); # Variable para el nombre de usuario
    configurar_ventana( ventana_2, "Selecciona tu usuario y compara" ,txt_login );
    usuario_tf_2 = credenciales_ventana_asistencia( ventana_2, usuario_2);

#Función para mandar los datos del usuario
def tomar_asistencia( usuario ):
    agregar = db.agregar_asistencia( usuario );
    if agregar :
        ms.showinfo("Asistencia", "Asistencia registrada");
    else:
        ms.showerror("Asistencia", "Error al registrar asistencia");
    ventana_2.destroy();
    
#Función para obtener el codigo de un usuario
def obtener_datos():
    #Checar si esta seleccionado un usuario
    if listbox.curselection() == (): 
        ms.showerror("Error", "Selecciona un usuario");
        #regresar a la misma ventana
        ventana_2.deiconify();
        return 0;
    usuario = listbox.get(listbox.curselection());
    #Obtener la codificacion del usuario de la BD;
    imagen_encode = db.obtener_usuario(usuario);
    # convertir imagen_encode en numpy array
    imagen_encode = np.fromstring(imagen_encode[1:-1], dtype=float, sep=' ');
    comparar_rostro( imagen_encode, usuario );

#Función para comparar el rostro del usuario con la imagen de la camara
def comparar_rostro( codigo_imagen, usuario):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW); # Iniciar camara
    bandera = False
    while True:
        ret, frame = cap.read();
        if ret == False: break;
        frame = cv2.flip(frame, 1); # Voltear la imagen
        cv2.putText(frame, "Presiona 'ESC' para salir", (10, 20), 4, 0.7, (255, 255, 255), 1);
        #Localizar rostro
        face_locations = fr.face_locations(frame); 
        if face_locations != []:
            for face_location in face_locations:
                face_frame_encodings = fr.face_encodings(frame, known_face_locations=[face_location])[0];
                resultado = fr.compare_faces([face_frame_encodings], codigo_imagen, tolerance=0.5);

                if resultado[0] == True:                    
                    bandera = True                    
                else:
                    text = "Desconocido";
                    color = (50, 50, 255);
                    cv2.rectangle(frame, (face_location[3], face_location[2]), (face_location[1], face_location[2] + 30), color, -1);
                    cv2.rectangle(frame, (face_location[3], face_location[0]), (face_location[1], face_location[2]), color, 2);
                    cv2.putText(frame, text, (face_location[3], face_location[2] + 20), 2, 0.7, (255, 255, 255), 1);
        
        if bandera: break;
        cv2.imshow("Comparacion", frame);
        k = cv2.waitKey(1);
        if k & 0xFF == 27: 
            break;
    
    if bandera:
        timer = hilo.Timer(1.0, tomar_asistencia, [usuario]);  
        timer.start();
    cap.release();
    cv2.destroyAllWindows();

#-------------------- Ventana principal --------------------
root.configure( bg = color_secundario );
Label( root, text = "¡BIENVENIDO!", font = ( font_label, 20 ), bg=color_primario , fg = color_white, width="500", pady="20").pack();
Label( root, text = "Escoja su opción", fg = color_white, font = ( font_label, 17 ),  width="500", pady="10" ,bg=color_primario ).pack();

#Widgtes
registro_btn = Button( root, text="Registrar", font = ( font_label, 17 ), width=30, height=2, borderwidth=3, relief="raised", fg = color_white, bg=color_terciario, command = registro);
login_btn  = Button( root, text="Acceder", font = ( font_label, 17 ), width=30, height=2, borderwidth=3, relief="raised", fg = color_white, bg=color_terciario, command = acceder );

#Marcadores 
getEnter( root );
getEnter( root );
registro_btn.pack();
getEnter( root );
getEnter( root );
login_btn.pack();


root.mainloop();