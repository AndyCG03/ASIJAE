Un asistente de consultas con información refrente a la universidad Tecnológica de la Habana José Antonio Echeverríá (cujae) que funciona usando 
TF-IDF (Term Frequency-Inverse Document Frequency) para vectorizar las preguntas y respuestas (Que decidi que debía conocer) y luego mediante 
la similitud del coseno se puede encontrar la pregunta más similar, a menos que exceda el umbral de similitud

Se emplean los contenidos aprendidos en la optativa de python como POO y el uso de matplotlib para representar como funciona el TF-IDF

Es importante entender que el asistente suele equivocarse mayormente cuando se le pregunta algo que no conoce por eso se da la retroalimentación
al usuario en la parte de ¨preguntas frecuentes¨ para que sepa de lo que es capaz de responder el asistente

El asistente es capaz de responder preguntas desde como matricularse en la universidad, becas, donde se podra comer, transporte y de algunos lugares
y eventos significativos

El resultado del proyecto es una aplicación de escritorio bastante visual e intuitiva que espero que le guste.

Pantalla Principal de la aplicación
![Captura de pantalla 2024-07-29 230926](https://github.com/user-attachments/assets/a014f979-a8fb-4ead-847b-17cf6491f464)

Ejemplo de uso con mostrado de graficado
![Captura de pantalla 2024-07-29 231009](https://github.com/user-attachments/assets/1eb0a3e3-0ce8-42a8-907a-c5fda4e62c13)

Ejemplo de pantalla Emergente 
![Captura de pantalla 2024-07-29 231024](https://github.com/user-attachments/assets/f8819c9c-dc63-4b32-b962-4641ce25fa99)

El proyecto también cuenta con efectos de sonidos y dentro del repo existe un video donde se muestra y explica su uso

Bibliotecas usadas
Trabajo con los Datos
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

Uso de efectos de sonido
import pygame

Trabajo con las pantallas de la aplicación
import tkinter as tk
from tkinter import scrolledtext, ttk
from PIL import Image, ImageTk

Trabajo con Graficas 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

Creado por Andy Clemente Gago 2do de Informática Optativa de Python tutora Lic. Sheila Leyva Sánchez
