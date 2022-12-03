#-------------------- Modulos --------------------
import cv2;
import face_recognition as fr;
import numpy as np;
from tkinter import *;
from tkinter import messagebox as ms;
import os;
from functools import partial
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

color_success = "/033[1;32;40m"
color_error = "/033[1;31;40m"
color_normal = "\033[0;37;40m"

root = Tk();
root.geometry( size_screen );
root.title( txt_title );

#-------------------- Funciones --------------------
def getEnter(screen):
    ''' Set an enter inside the screen '''
    Label(screen, text="", bg=color_secundario).pack()

def comprobarCredenciales( usuario ):
    # validar que el campo no este vacio y sean puras letras
    usuario = usuario.get();
    if usuario.isalpha():
        ventana_1.destroy();

#Función que configura las ventanas nuevas
def configurar_ventana( ventana, texto, titulo ):    
    ventana.geometry( size_screen );
    ventana.title( titulo );
    ventana.configure(bg=color_secundario);
    Label( ventana, text = texto, bg=color_primario, font = (font_label, 20), pady="20", fg = color_white, width=500 ).pack();

#Función que agrega los textos, cajas y botones de las nuevas ventanas
def credenciales( ventana, var, bandera ):
    getEnter( ventana );
    Label(ventana, text="Usuario:", fg=color_black, font = (font_label, 17), bg=color_secundario, pady="5").pack()
    entry = Entry(ventana, textvariable=var, justify=CENTER, font=(font_label, 15))
    entry.focus_force()
    entry.pack(side=TOP, ipadx=35, ipady=8)
    getEnter( ventana );
    getEnter( ventana );


    if bandera:
        Button(ventana, text="Comparar rostro", fg=color_white, bg=color_terciario, activebackground=color_black, borderwidth=0, font=(font_label, 14), height="2", width="35", command=acceder).pack()
        getEnter( ventana );
        Button( ventana, text="SALIR", fg=color_white, bg=color_red_btn, activebackground=color_red_btn_a, borderwidth=0, font=(font_label, 14), pady="2", width="14", command=ventana.destroy ).pack()
    else:
        Button(ventana, text="Capturar rostro", fg=color_white, bg=color_terciario, activebackground=color_black, borderwidth=0, font=(font_label, 14), height="2", width="35", command=registrar_imagen).pack()
        getEnter( ventana );
        getEnter( ventana );
        getEnter( ventana );
        getEnter( ventana );
        getEnter( ventana );
        getEnter( ventana );
        Button( ventana, text="SALIR", fg=color_white, bg=color_red_btn, activebackground=color_red_btn_a, borderwidth=0, font=(font_label, 14), pady="2", width="13", command=ventana.destroy ).pack()
    return entry


def registro():
    global usuario_1
    global usuario_tf_1
    global ventana_1
    
    ventana_1 = Toplevel(root); # Crear ventana
    usuario_1 = StringVar(); # Variable para el nombre de usuario

    configurar_ventana( ventana_1, "Ingrese sus datos" ,txt_register );
    usuario_tf_1 = credenciales( ventana_1, usuario_1, False );

def compararRostro():
    return 0;


#Función que ayuda a capturar la imagen
def registrar_imagen():
    bandera = True;
    cap =  cv2.VideoCapture(0, cv2.CAP_DSHOW); # Iniciar camara
    bandera = cap.isOpened(); # Verificar si la camara esta abierta
    # Agregar el nombre con 3 letras aleatorios
    nombre_imagen = usuario_1.get() + str(np.random.randint(100, 999)) + ".jpg";
    url_imagen = path + nombre_imagen;  
    
    while bandera:
        ret, frame = cap.read(); # Leer imagen
        #Mostrar texto en la imagen
        # cv2.putText(frame, "Presiona la tecla 's' para capturar la imagen", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA);
        cv2.putText(frame, "Presiona 's' para capturar o 'ESC' para salir", (10, 20), 4, 0.7, (255, 255, 255), 1);
        k = cv2.waitKey(1);
        if k & 0xFF == ord('s'): # Si se presiona la tecla "q" se toma la foto
            cv2.imwrite(url_imagen, frame); # Guardar imagen
            break;

        if k & 0xFF == 27: 
            bandera = False;
            print("Saliendo...");
            break;
        cv2.imshow("Registro", frame); # Mostrar imagen
    
    cap.release(); # Liberar camara
    cv2.destroyAllWindows(); # Cerrar ventana
    if bandera:
        procesar_imagen(url_imagen, nombre_imagen);

#Función que codifica la imagen y recibe la respuesta de la base de datos
def procesar_imagen(url_imagen, nombre):
    # print(url_imagen)
    imagen = cv2.imread(nombre); # Leer imagen
    nombre = nombre.replace(".jpg", "");
    # print(imagen); 
    if(fr.face_locations(imagen) == []):
        ventana_1.destroy();
        ms.showerror("Error", "No se detecto un rostro en la imagen");
        os.remove(url_imagen); # Eliminar imagen
        return 0;
    print(imagen);
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


def acceder():
    global usuario_2
    global usuario_tf_2
    global ventana_2

    ventana_2 = Toplevel(root); # Crear ventana
    usuario_2 = StringVar(); # Variable para el nombre de usuario
    configurar_ventana( ventana_2, "Ingresa tus datos" ,txt_login );
    usuario_tf_2 = credenciales( ventana_2, usuario_2, True );
    

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