class str_grammar:
    def __init__(self):
        self.VT = []
        self.VN = []
        self.P = {}
        self.S = ""
        self.loaded = False

    def free_memory(self):
        # Освобождаем память, выделенную под список VT
        if self.VT:
            del self.VT[:]
        
        # Освобождаем память, выделенную под список VN
        if self.VN:
            del self.VN[:]
        
        # Освобождаем память, выделенную под словарь P
        if self.P:
            self.P.clear()
    
    def load_grammar(self, vt, vn, p, s):
        self.VT = vt
        self.VN = vn
        self.P = p
        self.S = s
        self.loaded = True
    
    def count_non_term_sym(self, sequence):
        length = 0
        for char in sequence:
            if char in self.VT:
                length += 1
        return length
    
    def generate_chains(self, left_border, right_border, output, chain_history):
        from collections import deque, defaultdict

        rules = deque([self.S])
        used_sequences = set()
        sequence_history = defaultdict(str)
        sequence_history[self.S] = ""  # Начальная цепочка без предков

        while rules:
            sequence = rules.popleft()

            if sequence in used_sequences or len(sequence) > right_border:
                continue

            used_sequences.add(sequence)
            is_terminal = True

            for i, char in enumerate(sequence):
                if char in self.VN:
                    is_terminal = False

                    for replacement in self.P.get(char, []):
                        new_sequence = sequence[:i] + replacement + sequence[i+1:]

                        if new_sequence not in used_sequences and len(new_sequence) <= right_border:
                            rules.append(new_sequence)
                            sequence_history[new_sequence] = f"{sequence} -> {new_sequence}"

                    break

            if is_terminal and len(sequence) >= left_border:
                output.append(sequence)

                current = sequence
                chain = []
                while current:
                    chain.append(current)
                    current = sequence_history[current].split(' -> ')[0]
                if chain:
                    chain.reverse()
                    chain_history.append(" -> ".join(chain))
        return output
def generate_main(vt, vn, p, s, right_border):
    grammar = str_grammar()
    grammar.load_grammar(vt, vn, p, s)
    print(vt)
    print(vn)
    print(p)
    print(s)
    
    # Генерация цепочек
    left_border = 2
    output = []
    chain_history = []
    grammar.generate_chains(left_border, right_border, output, chain_history)

    # Вывод результата
    return output


# Создание экземпляра класса
grammar = str_grammar()

vt = ["a", "b"]
vn = ["S", "A"]
p = {"S": ["aA", "b"], "A": ["bS"]}
s = "S"
grammar.load_grammar(vt, vn, p, s)

# Генерация цепочек
left_border = 2
right_border = 6
output = []
chain_history = []
grammar.generate_chains(left_border, right_border, output, chain_history)

# Вывод результата
print("Generated Chains:")
for chain in output:
    print(chain)

print("\nChain History:")
for history in chain_history:
    print(history)

