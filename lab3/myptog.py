import json
from dataclasses import dataclass 
from typing import Dict, List
from tkinter import *
@dataclass
class Machine:
    Q: List[str]
    V: List[str]
    Func: Dict[str, Dict[str, str]]
    Start: str
    End: str
window_output_machine = Tk()
window_result = Tk()
res = []
def word_controll(word, machine, state, lbl2):
    if word == " ":
        print(f"({state}, {word})")
        print(f"Final state: {state}")
        if state in machine.End:
            print("all OK\n")
        else:
            raise ValueError("Error END\n")
        return

    print(f"({state}, {word})")
    if len(word) > 1:
        print(f"(δ({state},{word[0]}), {word[1:]})")
        try:
            state = machine.Func[state][word[0]]
        except KeyError:
            raise ValueError("Error can't go \n")
            return
        word = word[1:]
    else:
        print(f"(δ({state},{word[0]}),  )")
        try:
            state = machine.Func[state][word[0]]
        except KeyError:
            raise ValueError("Error can't go \n")
            return
        word = " "
    word_controll(word, machine, state, lbl2)

def file_reader(filename):
    try:
        with open(filename, "r") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        raise ValueError("Error file")
    states = data["states"]
    alphabet = data["alphabet"]
    func = data["Func"]
    start = data["start"]
    ends = data["ends"]
    machine = Machine(states, alphabet, func, start, ends)
    
    
    return machine

print("input the file name of <machine>.json")
window_output_machine.title("output")
window_result.title('result')
filename = input()
machine = file_reader(filename)
lbl1 = Label(window_output_machine,
             text=f"M({machine.Q}, {machine.V}, δ, {machine.Func}, ({machine.Start}){machine.End}", padx=5, pady=10)

lbl2 = Label()
print("input the sequens")
sequens = input()
if sequens == 'quit':
    exit(1)
if all([c in machine.V for c in sequens]):
    print("Starting")
    word_controll(sequens, machine, machine.Start,lbl2)
else:
    raise ValueError("\nInvalid inf\n")
lbl1.grid(row=1, column=0, sticky="w")
window_result.mainloop()
window_output_machine.mainloop()


