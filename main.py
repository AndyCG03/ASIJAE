from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk
import pygame
from tkinter import scrolledtext, ttk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

# Clase para procesar los Datos y se ve el uso de la POO
class ProcesarDatos():
    def __init__(self, file_path):
        self.file_path = file_path
        self.vectorizer = None
        self.tfidf_matrix = None
        self.respuestas = None

    # Función para cargar los Datos
    def cargarDatos(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            data = file.read().split('\n\n')

        preguntasRespuestas = []
        for item in data:
            lines = item.split('\n')
            pregunta = lines[0].replace('Pregunta: ', '')
            respuesta = lines[1].replace('Respuesta: ', '')
            preguntasRespuestas.append((pregunta, respuesta))

        return preguntasRespuestas

    # Método para entrenar al modelo
    def entrenarModelo(self, datos):
        preguntas = [pr[0] for pr in datos]
        respuestas = [pr[1] for pr in datos]

        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(preguntas)
        self.respuestas = respuestas

        return self.vectorizer, self.tfidf_matrix, self.respuestas

# ------------------------------------------------------------------------------

# INICIO los Datos procesados y activo el mixer de pygame
ubicacionDatos = "Datos/Datos.txt"
procesar_datos = ProcesarDatos(ubicacionDatos)
datosCargados = procesar_datos.cargarDatos()
vectorizer, tfidf_matrix, respuestas = procesar_datos.entrenarModelo(datosCargados)
pygame.mixer.init()

# LLAMAR A LA PANTALLA
# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Asistente de Consultas Cujae")
ventana.attributes('-fullscreen', True)  # Iniciar en pantalla completa
ventana.configure(bg="#333333")  # Cambiar a tu color preferido

# Añadir un Canvas para la imagen de fondo
canvas = tk.Canvas(ventana, bg="#333333", highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)

# Cargar la imagen de fondo
imagen_fondo = Image.open("img/fondo.jpg")
imagen_fondo = imagen_fondo.resize((ventana.winfo_screenwidth(), ventana.winfo_screenheight()),
                                   Image.Resampling.LANCZOS)
imagen_fondo = ImageTk.PhotoImage(imagen_fondo)
canvas.create_image(0, 0, anchor=tk.NW, image=imagen_fondo)

# Crear el cuadro de texto desplazable para mostrar los mensajes
cuadro_texto = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, state='disabled', bg="#E5E5E5", font=("Verdana", 14),
                                         borderwidth=0, highlightthickness=0, padx=15, pady=15)
cuadro_texto.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.6)

# ------------------------------------------------------------------------------

# Metodo para responder una pregunta
def responderPregunta(nueva_pregunta, vectorizer, tfidf_matrix, respuestas, umbral=0.35):
    nueva_pregunta_tfidf = vectorizer.transform([nueva_pregunta])
    similitudes = cosine_similarity(nueva_pregunta_tfidf, tfidf_matrix).flatten()

    idx_mejor_respuesta = similitudes.argmax()
    max_similitud = similitudes[idx_mejor_respuesta]

    if max_similitud >= umbral:
        mejorRespuesta = respuestas[idx_mejor_respuesta]

        if mostrar_graficas.get():
            # Obtener las funciones TF-IDF de la nueva pregunta y la mejor coincidencia
            mejor_pregunta_tfidf = tfidf_matrix[idx_mejor_respuesta].toarray().flatten()
            nueva_pregunta_tfidf = nueva_pregunta_tfidf.toarray().flatten()

            # Graficar las funciones TF-IDF
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(nueva_pregunta_tfidf, marker='o', label='Nueva Pregunta', color='red')
            ax.plot(mejor_pregunta_tfidf, marker='x', label='Mejor Coincidencia', color='green')
            ax.set_title('Funciones TF-IDF de la Nueva Pregunta y la Mejor Coincidencia')
            ax.set_xlabel('Índice del Término')
            ax.set_ylabel('Valor TF-IDF')
            ax.set_ylim(0, 1)
            ax.legend()

            root = tk.Tk()
            root.geometry("800x600")
            root.resizable(False, False)
            root.title("Comparación de la similitud de la pregunta de entrada con la de salida")
            root.attributes("-toolwindow", True)
            root.attributes("-topmost", True)

            frame = tk.Frame(root)
            frame.pack(fill=tk.BOTH, expand=True)

            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    else:
        mejorRespuesta = ("Lo siento, no tengo la información que buscas en este momento. "
                           "Por favor, intenta reformular tu pregunta.")

    return mejorRespuesta

# ------------------------------------------------------------------------------

#metodo para ejecutar el sonido de notificacion
def sonidoNotificacion():
    sonido = pygame.mixer.Sound("sounds/soundNotification.mp3")
    sonido.set_volume(1.0)
    sonido.play()

# ------------------------------------------------------------------------------

#metodo para ejecutar el sonido de presionar un boton
def sonidoBoton():
    sonido = pygame.mixer.Sound("sounds/click.mp3")
    sonido.set_volume(1.0)
    sonido.play()

# ------------------------------------------------------------------------------

# Función para manejar el envío de mensajes
def enviar_mensaje():
    if (entrada.get() != 'Escriba su pregunta...'):
        pregunta = entrada.get()
        if pregunta:
            sonidoNotificacion()
            mostrar_mensaje("\nUsuario:", pregunta)
            respuesta = responderPregunta(pregunta, vectorizer, tfidf_matrix,
                                          respuestas)  # Aquí llamamos a la función de respuesta
            mostrar_mensaje("\nAsistente:", respuesta)
            entrada.delete(0, tk.END)

# ------------------------------------------------------------------------------

# Funcion para mostrar los mensajes en el panel de texto
def mostrar_mensaje(sender, message):
    cuadro_texto.config(state='normal')
    cuadro_texto.insert(tk.END, f"{sender} {message}\n")
    cuadro_texto.config(state='disabled')
    cuadro_texto.yview(tk.END)

# ------------------------------------------------------------------------------

# Funcion para la pantalla de creador
def abrirCreador():
    sonidoBoton()
    dialogo = tk.Toplevel(ventana)
    dialogo.title("Información del Creador")
    dialogo.geometry("400x300")
    dialogo.config(bg='#016E51', borderwidth=0, highlightthickness=0)

    dialogo.resizable(False, False)

    # Cambiar el ícono del Toplevel
    icono = tk.PhotoImage(file="img/logo.png")
    dialogo.iconphoto(False, icono)

    # Centrar la ventana
    dialogo.update_idletasks()
    width = dialogo.winfo_width()
    height = dialogo.winfo_height()
    x = (ventana.winfo_screenwidth() // 2) - (width // 2)
    y = (ventana.winfo_screenheight() // 2) - (height // 2)
    dialogo.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    mensaje = tk.Label(dialogo,
                       text="Creado por:\nAndy Clemente Gago \n2do Año Ingeniería Informática\nTarea Final de Optativa: Python\n\nTutora:\n Lic. Sheila Leyva Sánchez",
                       fg='white', bg='#016E51', font=('Verdana', 14))
    mensaje.pack(pady=20)
    mensaje.place(relx=0.1, rely=0.2)

    # Hacer que el diálogo sea modal
    dialogo.grab_set()
    # Esperar a que el diálogo se cierre
    ventana.wait_window(dialogo)

# ------------------------------------------------------------------------------

# Funcion para la pantalla de las dudas
def abrirDudas():
    sonidoBoton()
    dialogo = tk.Toplevel(ventana)
    dialogo.title("Dudas Frecuentes")
    dialogo.geometry("1000x350")
    dialogo.config(bg='#016E51', borderwidth=0, highlightthickness=0)

    dialogo.resizable(False, False)

    # Cambiar el ícono del Toplevel
    icono = tk.PhotoImage(file="img/logo.png")
    dialogo.iconphoto(False, icono)

    # Centrar la ventana
    dialogo.update_idletasks()
    width = dialogo.winfo_width()
    height = dialogo.winfo_height()
    x = (ventana.winfo_screenwidth() // 2) - (width // 2)
    y = (ventana.winfo_screenheight() // 2) - (height // 2)
    dialogo.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    mensaje = tk.Label(dialogo,
                       text="Hola soy ASIJAE y te diré como puedes Usarme :)\nSi quiere saber más acerca de mi funcionamiento puede pedirme que le hable de mí.\n\n"
                            "Para formular una pregunta recuerde usar palabras claves para poder funcionar mejor\nEjemplo: '¿Qué carreras se estudian en la Cujae?'.\n\n"
                            "Fui creado incapaz de recordar mensajes anteriores y no me entreno conforme me pregunta.\n\nEspero con el tiempo seguir escalando y saber más temas de que hablar."
                            "\n\nRecuerde leer el documento de mi creador con la información de lo que soy capaz de responder.\n\nMuchas Gracias por leer hasta acá y buen día :D",
                       fg='white', bg='#016E51', font=('Verdana', 14), justify='left')
    mensaje.pack(anchor='nw', pady=20, padx=20)

    # Hacer que el diálogo sea modal
    dialogo.grab_set()
    # Esperar a que el diálogo se cierre
    ventana.wait_window(dialogo)

# ------------------------------------------------------------------------------

# Funcion para la pantalla de las preguntas
def abrirPreguntas():
    sonidoBoton()
    dialogo = tk.Toplevel(ventana)
    dialogo.title("Preguntas para hacer al modelo")
    dialogo.geometry("1200x600")
    dialogo.config(bg='#016E51', borderwidth=0, highlightthickness=0)

    dialogo.resizable(False, False)

    # Cambiar el ícono del Toplevel
    icono = tk.PhotoImage(file="img/logo.png")
    dialogo.iconphoto(False, icono)

    # Centrar la ventana
    dialogo.update_idletasks()
    width = dialogo.winfo_width()
    height = dialogo.winfo_height()
    x = (ventana.winfo_screenwidth() // 2) - (width // 2)
    y = (ventana.winfo_screenheight() // 2) - (height // 2)
    dialogo.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    # Crear un frame para contener el Text y el Scrollbar
    frame = tk.Frame(dialogo, bg='#016E51')
    frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Crear el widget Text con scroll
    texto_scroll = tk.Text(frame, wrap=tk.WORD, fg='white', bg='#016E51', font=('Verdana', 14), padx=10, pady=10)
    texto_scroll.insert(tk.END, "Preguntas que le puedo responder:\n"
                                "\n¿Qué carreras o facultades se estudian en Cujae?"
                                "\n¿Dónde está ubicada se encuentra Cujae?"
                                "\n¿instalaciones para practicar deportes?"
                                "\n¿Cómo me puedo matricular en la Cujae?"
                                "\n¿Cómo puedo saber más de la Cujae?"
                                "\n¿Hay becas disponibles Cujae?"
                                "\n¿Cómo puedo acceder la biblioteca Cujae?"
                                "\n¿Hay bibliotecas?"
                                "\n¿Qué instalaciones medicas tiene la cujae?"
                                "\n¿a quien puedo contactar o llamar para comunicarme con la universidad de la Cujae?"
                                "\n¿Puedo trabajar mientras estudio?"
                                "\n¿Actividades extracurriculares extra se hacen?"
                                "\n¿Qué transporte público puedo tomar para ir a la cujae?"
                                "\n¿Cuándo dan el carnet de estudiante FEU?"
                                "\n¿Qué opciones de comida hay cerca?"
                                "\n¿Cómo puedo participar en los movimientos estudiantiles?"
                                "\n¿Qué ingenierías se estudian o tienen en la Cujae?"
                                "\n¿El título de la Cujae tiene vigor en otros paises?"
                                "\n¿facilidades o privilegios tecnológicos que tienen los estudiantes de la Cujae?"
                                "\n¿Cuándo puedo a las ir canchas deportivas de la Cujae?"
                                "\n¿Cuál es la política de acoso o discriminación de la Cujae?"
                                "\n¿Cómo son prácticas profesionales o de curso en la Cujae?"
                                "\n¿Qué seguridad y protección hay en la Cujae?"
                                "\n¿A que hora empiezan las clases?"
                                "\n¿Qué son los juegos XIII de marzo?"
                                "\n¿Cuál es la Facultad más Sencilla?"
                                "\n¿Qué es el Festival de Cultura?"
                                "\n¿Cuánto duran las ingenierías?"
                                "\n¿Cómo Funcionas?"
                                "\n¿Cuál es tu Facultad favorita de la Cujae?"
                                "\n¿Qué es el Pasillo Central?"
                                "\n¿Qué es el Paso de los Vientos?"
                                "\n¿Qué es La Pecera?"
                                "\n¿Qué es El Cenicero?"
                                "\n¿La Cujae tiene Himno?"
                                "\n¿Cómo te llamas?"
                                "\n¿Cómo puedo becarme?"
                                "\n¿requisitos para inscribirme o matricularme en la Cujae?"
                                "\n¿Cómo puedo solicitar o pedir una beca en la Cujae?"
                                "\nHazme un chiste"
                                "\n¿Cuándo se inaugura la Cujae?"
                                "\n¿Cuál es la proyección de la Cujae?")

    texto_scroll.config(state=tk.DISABLED)  # Hacer que el Text sea solo de lectura
    texto_scroll.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Configurar el estilo del Scrollbar
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Vertical.TScrollbar",
                    background="#016E51",  # Color de fondo verde
                    bordercolor='#016E51',  # Color del borde
                    troughcolor='#016E51',  # Color del área de desplazamiento
                    arrowcolor='#016E51')  # Color de las flechas

    scrollbar = ttk.Scrollbar(frame, command=texto_scroll.yview, style="Vertical.TScrollbar")
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    texto_scroll.config(yscrollcommand=scrollbar.set)

    # Hacer que el diálogo sea modal
    dialogo.grab_set()
    # Esperar a que el diálogo se cierre
    ventana.wait_window(dialogo)

# ------------------------------------------------------------------------------

#funcion para limpiar la pantalla de lso textos
def limpiar_texto():
    sonidoBoton()
    cuadro_texto.config(state=tk.NORMAL)
    cuadro_texto.delete('1.0', tk.END)
    cuadro_texto.config(state=tk.DISABLED)
    mostrar_mensaje("Asistente:",
                    "Hola Bienvenido al Asistente de Consultas Cujae, siéntase libre de preguntarme cualquier duda que tenga.")
# ------------------------------------------------------------------------------

#PAra cerrar la aplicación
def cerrar_aplicacion():
    ventana.destroy()

# ------------------------------------------------------------------------------

# Función para manejar el enfoque en la entrada de texto
def on_entry_click(event):
    if entrada.get() == 'Escriba su pregunta...':
        entrada.delete(0, "end")  # Borrar el contenido
        entrada.config(fg='black')  # Cambiar el color del texto a negro

# ------------------------------------------------------------------------------

# Función para manejar la pérdida de enfoque en la entrada de texto
def on_focusout(event):
    if entrada.get() == '':
        entrada.insert(0, 'Escriba su pregunta...')  # Reinsertar el placeholder
        entrada.config(fg='grey')  # Cambiar el color del texto a gris

# ------------------------------------------------------------------------------

# Crear la entrada de texto para que el usuario escriba sus preguntas
pantallaEntrada = tk.Frame(ventana, bg="#FFFFFF")
pantallaEntrada.place(relx=0.1, rely=0.90, relwidth=0.7, relheight=0.05)

entrada = tk.Entry(pantallaEntrada, width=100, bg="#FFFFFF", font=("Verdana", 14), fg='grey', borderwidth=0)
entrada.insert(0, 'Escriba su pregunta...')  # Insertar el placeholder
entrada.bind('<FocusIn>', on_entry_click)  # Enfocar
entrada.bind('<FocusOut>', on_focusout)  # Desenfocar
entrada.pack(fill=tk.BOTH, expand=True, padx=50)

# Crear el botón de enviar
boton_enviar = tk.Button(ventana, text="Enviar", command=enviar_mensaje, font=("Verdana", 14))
boton_enviar.place(relx=0.825, rely=0.90, relwidth=0.075, relheight=0.05)

# Para enviar el mensaje al presionar Enter
entrada.bind('<Return>', lambda event: enviar_mensaje())

# Crear el botón de cerrar
boton_cerrar = tk.Button(ventana, text="X", command=cerrar_aplicacion, bg="red", fg="white", font=("Verdana", 14))
boton_cerrar.place(relx=0.965, rely=0.001, relwidth=0.035, relheight=0.05)

# Crear el botón de limpiar
boton_limpiar = tk.Button(ventana, text="Limpiar", command=limpiar_texto, font=("Verdana", 12))
boton_limpiar.place(relx=0.85, rely=0.765, relwidth=0.05, relheight=0.035)

mostrar_graficas = tk.BooleanVar()

#boton para mostrar graficas
boton_graficas = tk.Checkbutton(ventana, text="Ver gráficas", variable=mostrar_graficas, font=("Verdana", 12))
boton_graficas.place(relx=0.10, rely=0.765, relwidth=0.1, relheight=0.035)

# Boton dudas
labelDudas = tk.Label(ventana, text="Dudas", font=("Verdana", 14), fg='white', bg="#0E0E0E")
labelDudas.place(relx=0.6, rely=0.06, relwidth=0.05, relheight=0.05)
labelDudas.config(borderwidth=0, highlightthickness=0)

# Boton creador
labelCreador = tk.Label(ventana, text="Creador", font=("Verdana", 14), fg='white', bg="#0E0E0E")
labelCreador.place(relx=0.665, rely=0.06, relwidth=0.07, relheight=0.05)
labelCreador.config(borderwidth=0, highlightthickness=0)

# Boton Preguntas
labelPreguntas = tk.Label(ventana, text="Preguntas frecuentes", font=("Verdana", 14), fg='white', bg="#0E0E0E")
labelPreguntas.place(relx=0.75, rely=0.06, relwidth=0.15, relheight=0.05)
labelPreguntas.config(borderwidth=0, highlightthickness=0)

# Evento para el click en el boton dudas
labelDudas.bind("<Button-1>", lambda event: abrirDudas())
labelCreador.bind("<Button-1>", lambda event: abrirCreador())
labelPreguntas.bind("<Button-1>", lambda event: abrirPreguntas())
boton_graficas.bind("<Button-1>", lambda event: sonidoBoton())

# Cambiar el cursor al pasar por el Label
boton_graficas.bind("<Enter>", lambda event: boton_graficas.config(cursor="hand2"))
boton_graficas.bind("<Leave>", lambda event: boton_graficas.config(cursor=""))
labelDudas.bind("<Enter>", lambda event: labelDudas.config(cursor="hand2"))
labelDudas.bind("<Leave>", lambda event: labelDudas.config(cursor=""))
boton_cerrar.bind("<Enter>", lambda event: boton_cerrar.config(cursor="hand2"))
boton_cerrar.bind("<Leave>", lambda event: boton_cerrar.config(cursor=""))
boton_enviar.bind("<Enter>", lambda event: boton_enviar.config(cursor="hand2"))
boton_enviar.bind("<Leave>", lambda event: boton_enviar.config(cursor=""))
labelCreador.bind("<Enter>", lambda event: labelCreador.config(cursor="hand2"))
labelCreador.bind("<Leave>", lambda event: labelCreador.config(cursor=""))
labelPreguntas.bind("<Enter>", lambda event: labelPreguntas.config(cursor="hand2"))
labelPreguntas.bind("<Leave>", lambda event: labelPreguntas.config(cursor=""))
boton_limpiar.bind("<Enter>", lambda event: boton_limpiar.config(cursor="hand2"))
boton_limpiar.bind("<Leave>", lambda event: boton_limpiar.config(cursor=""))

# Mensaje de bienvenida del asistente
mostrar_mensaje("Asistente:",
                "Hola Bienvenido al Asistente de Consultas Cujae, siéntase libre de preguntarme cualquier duda que tenga.")

# Iniciar el bucle principal de la interfaz
ventana.mainloop()
