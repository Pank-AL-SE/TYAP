import re
from itertools import product

def generate_strings(regex, max_length):
    symbols = set(re.findall(r'\w', regex))
    strings = []
    
    for length in range(1, max_length + 1):
        for combination in product(symbols, repeat=length):
            string = ''.join(combination)
            if re.fullmatch(regex, string):
                strings.append(string)
                
    return strings
    
    