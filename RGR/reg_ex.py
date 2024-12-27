from typing import Set, List, Dict

import sys
from PyQt5.QtWidgets import QApplication, QWidget


def check_rules(rules, choice):
    if choice == 1:
        for rule in rules:
            control = rule.split('->')[1].split('|')
            for item in control:
                if len(item) == 2:
                    if str.istitle(item[0]) == False and str.istitle(item[1]) == True:
                        continue
                    elif str.isdigit(item[0]) == True and str.istitle(item[1]) == True:
                        continue
                    else:
                        raise ValueError("Не левосторонний")
                elif len(item) == 1:
                    if str.isdigit(item[0]) == True or str.istitle(item[0]) == True or str.istitle(item[0]) == False:
                        continue
                    else:
                        raise ValueError("Неизвестная ошибка")
    else:
        for rule in rules:
            control = rule.split('->')[1].split('|')
            for item in control:
                if len(item) == 2:
                    if str.istitle(item[1]) == False and str.istitle(item[0]) == True:
                        continue
                    elif str.isdigit(item[1]) == True and str.istitle(item[0]) == True:
                        continue
                    else:
                        raise ValueError("Не правосторонний")
                elif len(item) == 1:
                    if str.isdigit(item[0]) == True or str.istitle(item[0]) == True or str.istitle(item[0]) == False:
                        continue
                    else:
                        raise ValueError("Неизвестная ошибка")
# Структура для хранения грамматики
class Grammar:
    def __init__(self):
        self.terminals: Set[str] = set()  # Множество терминалов
        self.non_terminals: Set[str] = set()  # Множество нетерминалов
        self.rules: Dict[str, List[str]] = {}  # Правила грамматики
        self.start_symbol: str = ""  # Начальный символ

rg = Grammar()

# Функция для поиска всех конечных цепочек терминалов
def find_terminal_chains(non_terminal: str, current_chain: str, visited: Set[str], terminal_chains: List[str], depth: int = 0):
    MAX_DEPTH = 100  # Максимальная глубина рекурсии
    if depth > MAX_DEPTH:
        return

    if non_terminal in visited:
        return  # Если узел уже посещён, не продолжаем

    visited.add(non_terminal)
    for rule in rg.rules.get(non_terminal, []):
        new_chain = current_chain
        all_terminals = True

        for ch in rule:
            if ch.isupper():  # Если символ является нетерминалом
                all_terminals = False
                find_terminal_chains(ch, new_chain, visited, terminal_chains, depth + 1)
                break
            else:  # Если символ является терминалом
                new_chain += ch

        if all_terminals:
            terminal_chains.append(new_chain)

    visited.remove(non_terminal)  # Убираем из посещённых
MAX_DEPTH = 100  # Максимальная глубина рекурсии

# Основная функция для построения регулярного выражения
def expand(non_terminal: str, current_chain: str, visited: Set[str], results: List[str], depth: int = 0):
    if depth > MAX_DEPTH:
        return

    if non_terminal in visited:
        if current_chain:
            terminal_chains = []
            temp_visited = set()
            find_terminal_chains(non_terminal, "", temp_visited, terminal_chains)

            for chain in terminal_chains:
                results.append(f"({current_chain})*{chain}")
        return

    visited.add(non_terminal)
    for rule in rg.rules.get(non_terminal, []):
        new_chain = current_chain
        all_terminals = True

        for ch in rule:
            if ch.isupper():  # Если символ является нетерминалом
                all_terminals = False
                expand(ch, new_chain, visited, results, depth + 1)
                break
            else:  # Если символ является терминалом
                new_chain += ch

        if all_terminals:
            results.append(new_chain)

    visited.remove(non_terminal)  # Убираем из посещённых

def find_terminal_chains_rl(non_terminal: str, current_chain: str, visited: Set[str], terminal_chains: List[str], depth: int = 0):
    if depth > MAX_DEPTH:
        return

    if non_terminal in visited:
        return  # Если узел уже посещён, не продолжаем

    visited.add(non_terminal)
    for rule in reversed(rg.rules.get(non_terminal, [])):  # Обрабатываем правила справа налево
        new_chain = current_chain
        all_terminals = True

        for ch in reversed(rule):  # Обрабатываем символы в правиле справа налево
            if ch.isupper():  # Если символ является нетерминалом
                all_terminals = False
                find_terminal_chains_rl(ch, new_chain, visited, terminal_chains, depth + 1)
                break
            else:  # Если символ является терминалом
                new_chain = ch + new_chain  # Добавляем терминал справа

        if all_terminals:
            terminal_chains.append(new_chain)

    visited.remove(non_terminal)  # Убираем из посещённых


# Основная функция для построения регулярного выражения
def expand_rl(non_terminal: str, current_chain: str, visited: Set[str], results: List[str], depth: int = 0):
    if depth > MAX_DEPTH:
        return

    if non_terminal in visited:
        if current_chain:
            terminal_chains = []
            temp_visited = set()
            find_terminal_chains_rl(non_terminal, "", temp_visited, terminal_chains)

            for chain in terminal_chains:
                results.append(f"{chain}({current_chain})*")
        return

    visited.add(non_terminal)
    for rule in reversed(rg.rules.get(non_terminal, [])):  # Обрабатываем правила справа налево
        new_chain = current_chain
        all_terminals = True

        for ch in reversed(rule):  # Обрабатываем символы в правиле справа налево
            if ch.isupper():  # Если символ является нетерминалом
                all_terminals = False
                expand_rl(ch, new_chain, visited, results, depth + 1)
                break
            else:  # Если символ является терминалом
                new_chain = ch + new_chain  # Добавляем терминал справа

        if all_terminals:
            results.append(new_chain)

    visited.remove(non_terminal)  # Убираем из посещённых

def convert_to_dict(rules):
    res_dict = {}
    for rule in rules:
        res_dict[rule.split("->")[0]] = rule.split("->")[1].split("|")
    return res_dict


def get_start_symbol(rules):
    for keys in rules.keys():
        return keys



def generator(choice: int, rules: str):
    rules = rules.split()
    # Инициализация грамматики
    check_rules(rules, choice)

    # rg.terminals = {"a", "b", "c", "d"}
    # rg.non_terminals = {"S", "A", "B", "C"}
    # rg.rules = {
    #     "S": ["aA", "b"],
    #     "A": ["cB", "z"],
    #     "B": ["mS"]
    # }

    rg.rules = convert_to_dict(rules)
    rg.start_symbol = get_start_symbol(rg.rules)

    
    results = []  # Список для хранения результатов
    visited = set()  # Множество для отслеживания посещённых узлов

    if choice == 1:
        expand(rg.start_symbol, "", visited, results)
    else:
        expand_rl(rg.start_symbol, "", visited, results)

    # Убираем дубликаты и объединяем результаты
    unique_results = set(results)

    return unique_results

