from dataclasses import dataclass
from typing import Dict, List
from tkinter import *
from tkinter import filedialog
from os import path
from functools import partial
from colorama import Fore, init
import json

nomachine = 0
window = Tk()
txt = Entry(master=window, width=60)
text = Text(master=window, width=60, height=10)


@dataclass
class Machine:
    Q: List[str]
    V: List[str]
    Rules: List[List[str]]
    Start_state: str
    Current_state: str
    Start_stack: str
    Stack: str
    End: str


def machine_input(filename):
    try:
        with open(filename, "r") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        print("Файл с данными не найден.")
        exit(-1)
    states = data["states"]
    alphabet = data["alphabet"]
    in_stack = data["in_stack"]
    rules = data["rules"]
    start = data["start"]
    stack = data["start_stack"]
    end = data["end"]
    lbl_machine = Label(window, text=f"P({states}, {alphabet}, {in_stack}, δ, {start}, {stack}, {end})",
                        font=("Arial", 15), padx=5, pady=10)
    lbl_machine.grid(row=1, column=0, sticky="w")
    print(f"P({states}, {alphabet}, {in_stack}, δ, {start}, {stack}, {end})")
    for i in rules:
        if i[1] == "EPS":
            i[1] = "del"
        if i[4] == "EPS":
            i[4] = "del"
        print(f"({i[0]}, {i[1]}, {i[2]}) -> ({i[3]}, {i[4]})")
    machine = Machine(states, alphabet, rules, start, start, stack, stack, end)
    return machine





def clicked():
    file = filedialog.askopenfilename(filetypes=[("Json Files", "*.json"), ("All Files", "*.*")],
                                      initialdir=path.dirname(__file__))
    if not file:
        return
    result = machine_input(file)
    frame = Frame(master=window, padx=10, pady=15)
    frame.grid(row=2, column=0, sticky="w")
    lbl_check_word = Label(window, text=f" INPUT string: ", font=("Arial", 15), padx=5, pady=10)
    lbl_check_word.grid(row=3, column=0, sticky="w")
    txt.grid(row=4, column=0)
    btn_check_word = Button(window, text="Check", command=partial(check_button, result), padx=10, pady=10)
    btn_check_word.grid(row=4, column=1, sticky="e")

    


def check_button(machine):
    text = txt.get()
    if text == 'quit':
        return 0
    machine.Current_state = machine.Start_state
    machine.Stack = machine.Start_stack
    if all([c in machine.V for c in text]):
        check_word(text, machine)
    else:
        raise ValueError("\nSymb not in alf\n")


def check_word(word, machine):
    print("Stack:", machine.Stack, "\n")
    step = 1
    for i in word:
        r_s = 0
        print("Chain:", i)
        print("Current stack:", machine.Stack)
        for j in machine.Rules:
            print(machine.Current_state, j[0])
            if machine.Current_state != j[0]:
                r_s += 1
                continue
            print(i, j[1])
            if i != j[1]:
                r_s += 1
                continue
            print(machine.Stack[0], j[2])
            if machine.Stack[0] != j[2]:
                r_s += 1
                continue

            print(f"Rule: ({j[0]}, {j[1]}, {j[2]}) -> ({j[3]}, {j[4]})\n")
            
            machine.Current_state = j[3]
            if len(j[4]) == 2:
                machine.Stack = i + machine.Stack
            elif j[4] == "del":
                machine.Stack = machine.Stack[1:]
            break
        step += 1
        if r_s == len(machine.Rules):
            raise AttributeError("Can't go to any state\n")
    while TRUE:
        if len(machine.Stack) == 0 and machine.Current_state == machine.End:
            return
        r_s = 0
        for j in machine.Rules:
            if machine.Current_state != j[0]:
                r_s += 1
                continue
            if "del" != j[1]:
                r_s += 1
                continue
            if machine.Stack[0] != j[2]:
                r_s += 1
                continue

            print(f"Rule: ({j[0]}, {j[1]}, {j[2]}) -> ({j[3]}, {j[4]})\n")
            machine.Current_state = j[3]
            if j[4] == "del":
                machine.Stack = machine.Stack[1:]
                break
        step += 1
        if r_s == len(machine.Rules):
            raise AttributeError("Can't go any state\n")


# ζ δ del
if __name__ == '__main__':
    window.title("")
    lbl = Label(window, text="Upload:", font=("Arial Bold", 20))
    lbl.grid(row=5, column=0, sticky="nw")
    btn = Button(window, text="update", command=clicked, padx=10, pady=10)
    btn.grid(row=5, column=1, sticky="e")
    window.mainloop()