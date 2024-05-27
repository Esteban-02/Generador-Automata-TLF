import tkinter as tk
from tkinter import ttk
import pydot
from PIL import Image, ImageTk
import re
from collections import defaultdict
from lexer import Lexer
from AutomatonVisualizer import AutomatonVisualizer

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Analizador Léxico")
        self.geometry("1200x800")

        self.lexer = Lexer()
        self.visualizer = AutomatonVisualizer()
        
        self.tokens_list = []

        self.input_label = tk.Label(self, text="Ingrese el código fuente:")
        self.input_label.pack(pady=10)
        
        self.input_text = tk.Text(self, width=100, height=10)
        self.input_text.pack(pady=10)

        self.send_button = tk.Button(self, text="Analizar", command=self.analyze_text)
        self.send_button.pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("Token", "Categoría"), show="headings")
        self.tree.heading("Token", text="Token")
        self.tree.heading("Categoría", text="Categoría")
        self.tree.pack(pady=10)

        self.clear_button = tk.Button(self, text="Limpiar", command=self.clear_screen)
        self.clear_button.pack(pady=10)

        self.automata_label = tk.Label(self, text="Autómata:")
        self.automata_label.pack(pady=10)
        self.automata_canvas = tk.Canvas(self, width=800, height=400)
        self.automata_canvas.pack(pady=10)

    def analyze_text(self):
        text = self.input_text.get("1.0", tk.END).strip()
        if text:
            self.tokens_list.clear()
            for row in self.tree.get_children():
                self.tree.delete(row)

            tokens = self.lexer.tokenize(text)
            for token in tokens:
                self.tokens_list.append((token.value, token.type))
                category = self.lexer.token_descriptions.get(token.type, token.type)
                self.tree.insert("", "end", values=(token.value, category))
            
            self.visualizer.draw_combined_automaton(tokens, 'combined_automaton.png')
            self.visualizer.display_automaton(self.automata_canvas, 'combined_automaton.png')

    def clear_screen(self):
        self.input_text.delete("1.0", tk.END)
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.tokens_list.clear()
        self.automata_canvas.delete("all")

if __name__ == "__main__":
    app = Application()
    app.mainloop()