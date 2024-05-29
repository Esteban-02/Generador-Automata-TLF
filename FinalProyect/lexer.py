import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pydot
from PIL import Image, ImageTk
import re
from collections import defaultdict


    # Esta clase se utiliza para crear objetos que representan tokens individuales. 
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
        
    # Esta clase Esta define cómo funciona el analizador léxico
    # especificando los tipos de tokens y sus expresiones regulares correspondientes

class Lexer:
    def __init__(self):
        self.token_specification = [
            
            # se especifica la categoria y los tokens que tiene cada categoria 
            ('Operadores_aritméticos', r'S\+|R\-|M\*|D\/|P\%|E\^'),
            ('Operadores_relacionales', r'>>|<<|>>=|<<=|<==>|!='),
            ('Operadores_lógicos', r'YY|OO|NO'),
            ('Operadores_de_asignación', r'==|S\+=|R\-=|M\*=|D\/=|P\%=|E\^='),
            ('Símbolos_de_abrir', r'\('),
            ('Símbolos_de_cerrar', r'\)'),
            ('Terminal_y_o_inicial', r';'),
            ('Separadores_de_sentencias', r','),
            ('Palabra_reservada_para_bucle_o_ciclo', r'\b(PARA|MIENTRAS)\b'),
            ('Palabra_para_decisión', r'\b(SI|ENTONCES|SINO|SINO_SI|FIN_SI)\b'),
            ('Palabra_para_la_clase', r'\b(CLASE|FIN_CLASE|ABSTRACTO|FIN_ABSTRACTO|INTERFACE|FIN_INTERFACE)\b'),
            ('Identificador_de_variable', r'\bVR\b'),
            ('Identificador_de_método', r'\bMETODO\b'),
            ('Identificador_de_clase', r'\b(CLASE|ABSTRACTO|INTERFACE)\b'),
            ('Enteros', r'\b(entero|logaritmo|crto|byte)\b'),
            ('Reales', r'\b(flotante|doble)\b'),
            ('Cadenas_de_caracteres_con_3_caracteres_especiales', r'}n|}t|}s'),
            ('Caracteres', r'\bcaracter\b'),
            ('Palabra_para_los_enteros', r'\b(ent|lgo|crto|byte)\b'),
            ('Palabra_para_los_reales', r'\b(flot|dbl)\b'),
            ('Cadenas_de_caracteres', r'\b(cdna)\b'),
            ('Palabra_para_los_caracteres', r'\b(crte)\b'),
            ('Palabra', r'\b[A-Za-z_]\w*\b'),
            ('NUMBER', r'\b\d+(\.\d*)?\b'),
            ('COMMENT', r'//.*?$|/\*.*?\*/'),
            ('NEWLINE', r'\n'),
            ('SKIP', r'[ \t]+'),  # Ignorar espacios en blanco
            ('MISMATCH', r'.'),   # Manejar cualquier otro carácter no reconocido
            
            
        ]
        
        # Cambia el _ por un espacio en blanco para mostrar en la tabla
        self.token_descriptions = {spec[0]: spec[0].replace('_', ' ') for spec in self.token_specification}


    # El propósito de este método es analizar una cadena de texto que ingresa el usuario y dividirla en una 
    # secuencia de tokens según las especificaciones de los tokens definidas en la clase lexer
    def tokenize(self, text):
        tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in self.token_specification)
        get_token = re.compile(tok_regex, re.DOTALL | re.MULTILINE).finditer
        tokens = []

        for mo in get_token(text):
            kind = mo.lastgroup
            value = mo.group(kind)
            if kind == 'NEWLINE' or kind == 'SKIP':
                continue
            if kind == 'MISMATCH':
                # Lanza una ventana emergente con el mensaje de error
                messagebox.showerror("Error", f"Token no encontrado: {value!r}")
                raise RuntimeError(f'Token no encontrado: {value!r}')
            tokens.append(Token(kind, value))
        return tokens