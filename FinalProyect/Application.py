#                   ANALIZADOR 
#                       Lexico
#
#Presentado por: David Serna Restrepo
#                Esteban Julian Ortega
#
#Presentado a: Ana Maria Tamayo

# Programa que analiza una cadena de caracteres, identifica 


import tkinter as tk
from tkinter import ttk
import pydot
from PIL import Image, ImageTk
import re
from collections import defaultdict
from lexer import Lexer
from AutomatonVisualizer import AutomatonVisualizer

#Se encarga de iniciar la logica del programa y de mostrar la interfaz grafica del analizador

class Application(tk.Tk):
    
    # Metodo que crea la interfaz grafica con los campos necesarios para mostrar los resultados
    def __init__(self):
        super().__init__()
        self.title("Analizador Léxico")
        self.geometry("900x800")
        
    # inicia las clases clases que se usaran
        self.lexer = Lexer()
        self.visualizer = AutomatonVisualizer()
    # Se declara una lista para los tokens  
        self.tokens_list = []

    # Creacion del Texxt para ingresar el texto
        self.input_label = tk.Label(self, text="Ingrese el código fuente:")
        self.input_label.pack(pady=10)
        
        self.input_text = tk.Text(self, width=80, height=3)
        self.input_text.pack(pady=10)
    # declara el boton analizar
        self.send_button = tk.Button(self, text="Analizar", command=self.analyze_text)
        self.send_button.pack(pady=10)
    # Crea la tabla de analisis
        self.tree = ttk.Treeview(self, columns=("Token", "Categoría"), show="headings")
        self.tree.heading("Token", text="Token")
        self.tree.heading("Categoría", text="Categoría")
        self.tree.pack(pady=10)
    # crea el boton limpiar pantalla
        self.clear_button = tk.Button(self, text="Limpiar", command=self.clear_screen)
        self.clear_button.pack(pady=10)
    # recerva el espacio para el automama en la interfaz
        self.automata_label = tk.Label(self, text="Autómata:")
        self.automata_label.pack(pady=10)
        self.automata_canvas = tk.Canvas(self, width=800, height=400)
        self.automata_canvas.pack(pady=10)

    #metodo que analiza el texto y lo transforma en palabras sin espacios para luego ser analizadas
    def analyze_text(self):
        text = self.input_text.get("1.0", tk.END).strip()
        if text:
    #Limpia la interfaz de tokens viejos
            self.tokens_list.clear()
            for row in self.tree.get_children():
                self.tree.delete(row)
    # Genera los nuevos tokens del texto que el usuario ingreso 
            tokens = self.lexer.tokenize(text)
            for token in tokens:
                self.tokens_list.append((token.value, token.type))
                category = self.lexer.token_descriptions.get(token.type, token.type)
                self.tree.insert("", "end", values=(token.value, category))
    # crea un automata       
            self.visualizer.draw_combined_automaton(tokens, 'combined_automaton.png')
            self.visualizer.display_automaton(self.automata_canvas, 'combined_automaton.png')

    #Metodo para limpiar la pantalla y dejarla lista para el siguiente analisis
    def clear_screen(self):
        self.input_text.delete("1.0", tk.END)
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.tokens_list.clear()
        self.automata_canvas.delete("all")

if __name__ == "__main__":
    app = Application()
    app.mainloop()