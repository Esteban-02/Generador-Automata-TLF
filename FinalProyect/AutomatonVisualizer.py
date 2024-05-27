import tkinter as tk
from tkinter import ttk
import pydot
from PIL import Image, ImageTk
import re
from collections import defaultdict

class AutomatonVisualizer:
    def __init__(self):
        pass

    def draw_combined_automaton(self, tokens, filename):
        graph = pydot.Dot(graph_type='digraph', rankdir='LR')
        graph.set_node_defaults(shape='circle')
        
        initial_state = 'S0'
        graph.add_node(pydot.Node(initial_state))
        current_state = initial_state
        node_count = 1
        state_dict = {initial_state: initial_state}

        for token in tokens:
            token_value = token.value
            i = 0
            while i < len(token_value):
                char = token_value[i]
                next_state = f'S{node_count}'

                # Check for repetition to form a loop
                repeat_count = 1
                while i + 1 < len(token_value) and token_value[i + 1] == char:
                    repeat_count += 1
                    i += 1
                
                if repeat_count > 1:
                    # Create a loop if the character repeats
                    graph.add_edge(pydot.Edge(current_state, current_state, label=char))
                else:
                    if next_state not in state_dict:
                        graph.add_node(pydot.Node(next_state))
                        state_dict[next_state] = char
                    graph.add_edge(pydot.Edge(current_state, next_state, label=char))
                    current_state = next_state
                    node_count += 1
                
                i += 1
            
            # Mark the final state of the current token
            graph.add_node(pydot.Node(current_state, shape='doublecircle'))
            current_state = initial_state  # Reset to start state for the next token

        graph.write_png(filename)

    def display_automaton(self, canvas, path):
        img = Image.open(path)
        img = img.resize((600, 200), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        canvas.image = img_tk