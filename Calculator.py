import tkinter as tk
from tkinter import *
import re

def parse_expression(In):
    tokens = re.findall(r'([-+*/^])\s*([-+*/^])\s*(\d*\.?\d+)|(\d*\.?\d+|[-+*/^()])', In)
    i = 0
    for token in tokens:
        tokens[i] = list(token)
        tokens[i] = [ele for ele in tokens[i] if ele != '']
        if len(tokens[i]) > 2:
            tokens[i][-1] = tokens[i][-2] + tokens[i][-1]
            tokens[i].pop(-2)
            tokens.insert(i, tokens[i][-1])
            tokens.insert(i, [tokens[i+1][0]])
            tokens.pop(i+2)
        if len(tokens[i]) == 2:
            tokens[i] = [tokens[i][0] + tokens[i][-1]]

        tokens[i] = tokens[i][0]
        i+=1

    return Format(tokens)

def Format(In):
    Equation = []
    Bracket = False
    Temp = []
    for i in range(len(In)):
        if In[i] == "(":
            Bracket = True
        elif In[i] == ")":
            Bracket = False
            Equation.append(Temp)
            Temp = []
        elif Bracket:
            Temp.append(In[i])
        else:
            Equation.append(In[i])
    
    return Equation

def Brackets(Equation):
    for i in range(len(Equation)):
        if type(Equation[i]) == list:
            Equation[i] = Indicies(Equation[i])
            if len(Equation[i]) == 1:
                Equation[i] = str(Equation[i][0])

            Equation[i] = Divide(Equation[i])
            if len(Equation[i]) == 1:
                Equation[i] = str(Equation[i][0])

            Equation[i] = Multiply(Equation[i])
            if len(Equation[i]) == 1:
                Equation[i] = str(Equation[i][0])
            
            Equation[i] = Addition_Subtraction(Equation[i])
            if len(Equation[i]) == 1:
                Equation[i] = str(Equation[i][0])
        
    if "(" not in Equation:
        Equation = Indicies(Equation)

        Equation = Divide(Equation)

        Equation = Multiply(Equation)
        
        Equation = Addition_Subtraction(Equation)
    
    return Equation

def Indicies(Equation):
    i = 0
    while i <= len(Equation)-1:
        if Equation[i] == "^":
            Temp = float(Equation[i-1]) ** float(Equation[i+1])
            Equation[i-1] = Temp
            Equation.pop(i)
            Equation.pop(i)
            i -= 2
        i+=1
    return Equation

def Divide(Equation):
    i = 0
    while i <= len(Equation)-1:
        if Equation[i] == "/":
            if float(Equation[i+1]) == 0:
                raise ZeroDivisionError("Division by zero encountered.")
            Temp = float(Equation[i-1]) / float(Equation[i+1])
            Equation[i-1] = Temp
            Equation.pop(i)
            Equation.pop(i)
            i -= 2
        i+=1
    return Equation

def Multiply(Equation):
    i = 0
    while i <= len(Equation)-1:
        if Equation[i] == "*":
            Temp = float(Equation[i-1]) * float(Equation[i+1])
            Equation[i-1] = Temp
            Equation.pop(i)
            Equation.pop(i)
            i -= 2
        i+=1
    return Equation

def Addition_Subtraction(Equation):
    i = 0
    while i <= len(Equation)-1:
        if Equation[i] == "-":
            Temp = float(Equation[i-1]) - float(Equation[i+1])
            Equation[i-1] = Temp
            Equation.pop(i)
            Equation.pop(i)
            i -= 2
        elif Equation[i] == "+":
            Temp = float(Equation[i-1]) + float(Equation[i+1])
            Equation[i-1] = Temp
            Equation.pop(i)
            Equation.pop(i)
            i -= 2
        i+=1
    return Equation

def start_move(event):
    global x, y
    x = event.x
    y = event.y

def stop_move(event):
    global x, y
    x = None
    y = None

def move_window(event):
    global x, y
    dx = event.x - x
    dy = event.y - y
    x0 = root.winfo_x() + dx
    y0 = root.winfo_y() + dy
    root.geometry(f"+{x0}+{y0}")

def on_button_click(char):
    current_text = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current_text + char)

def evaluate_expression():
    try:
        parse = parse_expression(entry.get().replace('x', '*').replace('^', '**'))
        result = Brackets(parse)[0]
        try:
            result = int(result)
        except:
            pass
        equation.delete(0, tk.END)
        equation.insert(0, str(entry.get()))
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
    except Exception as e:
        equation.delete(0, tk.END)
        equation.insert(0, str(entry.get()))
        entry.delete(0, tk.END)
        entry.insert(0, "Error")

def clear():
    entry.delete(0, tk.END)

root = tk.Tk()
root.overrideredirect(True)
root.geometry('400x350+200+200')

# Title bar
title_bar = Frame(root, bg='#2b2b2b', relief='raised', bd=0)
title_bar.pack(fill=tk.X)
title_bar.bind('<B1-Motion>', move_window)
title_bar.bind('<Button-1>', start_move)
title_bar.bind('<ButtonRelease-1>', stop_move)

# Title label
title_label = Label(title_bar, text='Calculator', fg='white', bg='#2b2b2b', font=('Helvetica', 12))
title_label.pack(side=LEFT, padx=10)

# Close button
close_button = Button(title_bar, text='✕', font=('Helvetica', 12), width=4, relief='flat', bg="#2b2b2b", fg="white", borderwidth=0, command=root.destroy)
close_button.pack(side=RIGHT)

# Entry widget
entry = Entry(root, font=('Helvetica', 16), justify='right', bd=4)
entry.pack(expand=True, fill=tk.X, padx=10, pady=(10, 0))

# Equation widget
equation = Entry(root, font=('Helvetica', 12, 'bold'), justify='right', bd=4)
equation.pack(expand=True, fill=tk.X, padx=10, pady=(0, 10))

# Buttons frame
buttons_frame = Frame(root)
buttons_frame.pack(expand=True, fill=tk.BOTH)

# Buttons
button_texts = [
    ('7', '8', '9', '/', '('),
    ('4', '5', '6', 'x', ')'),
    ('1', '2', '3', '-', '^'),
    ('.', '0', 'C', '=', '+')
]

# Create buttons
for row in button_texts:
    row_frame = Frame(buttons_frame)
    row_frame.pack(expand=True, fill=tk.X)
    for char in row:
        if char == "C":
            btn = Button(row_frame, text=char, font=('Helvetica', 14), relief='flat', width=5, height=2,
                         command=lambda ch=char: clear())
            btn.pack(side=LEFT, expand=True, fill=tk.BOTH)
        elif char:
            btn = Button(row_frame, text=char, font=('Helvetica', 14), relief='flat', width=5, height=2,
                         command=lambda ch=char: on_button_click(ch) if ch != '=' else evaluate_expression())
            btn.pack(side=LEFT, expand=True, fill=tk.BOTH)
        else:
            Label(row_frame, text='', width=5, height=2).pack(side=LEFT, expand=True, fill=tk.BOTH)

root.mainloop()
