from gramma import Grammar

def opration(grammar,lb,rb):
    rules = list(grammar.S)
    used_seq = set()
    res = []
    while rules:
        seq = rules.pop()
        if seq in used_seq:
            continue
        used_seq.add(seq)
        no_term = True
        for i, symbol in enumerate(seq):
            if symbol in grammar.VN:
                no_term = False
                for elem in grammar.P[symbol]:
                    temp = seq[:i] + elem + seq[i + 1:]
                    if grammar.count_non_term_sym(grammar, temp) <= rb and temp not in rules:
                        rules.append(temp)
            elif symbol not in grammar.VT:
                no_term = False
                res.append( "цепочка " + seq + " не разрешима")
                break
        if no_term and lb <= len(seq) <= rb:
            res.append(seq if seq else "лямбда")
    return res


