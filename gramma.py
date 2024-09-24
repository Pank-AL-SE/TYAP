from typing import Dict, List

class Grammar():

    def __init__(self):
        self.VT: List[str]
        self.VN: List[str]
        self.P: Dict[str, List[str]]
        self.S: str


            
    def grammar_input(self):
        result = dict()
        VT = list(map(str, input("Введите терминальные символы: ").split()))
        VN = list(map(str, input("Введите не терминальные символы: ").split()))
        n = int(input("Введите количество правил: "))
        P = dict()
        for _ in range(n):
            r = input("Введите терминал правила: ")
            rs = input("Введите правило:").split()
            P[r] = rs
        S = str(input("Введите целевой символ: "))
        VT.append("_")
        return {"VT": VT, "VN": VN, "P": P, "S": S}


    def count_non_term_sym(self, grammar, sequence):
        length = 0
        for sym in sequence:
            if sym in grammar.VT:
                length += 1
        return length
    
    
    def simple_grammar(self):
        self.VT = ["0", "1"]
        self.VN = ["A", "B"]
        self.P = {"A": ["0A1A", "1A0A", ""]}
        self.S = "A"

    def output(self):
        return self.VT, self.VN, self.P, self.S