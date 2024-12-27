import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QMainWindow, QLabel, QComboBox, QPlainTextEdit, QPushButton
from reg_ex import generator, get_start_symbol, convert_to_dict
from string_generator import generate_strings
from generate_from_rules import generate_main
from read_json import read_json
from PyQt5.QtGui import QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Курсовая работа. Панк Александр Сергеевич. Вариант 12")
        self.resize(580, 920)

        self.terminal_lbl = QLabel('Введите терминальные символы:', self)
        self.terminal_lbl.move(20,10)
        self.terminal_lbl.resize(260, 20)

        # Создаем строку grammar
        self.input_terminal = QLineEdit(self)
        self.input_terminal.move(20, 30)
        self.input_terminal.resize(260, 40)

        self.nonterminal_lbl = QLabel('Введите нетерминальные:', self)
        self.nonterminal_lbl.move(20,70)
        self.nonterminal_lbl.resize(260, 20)

        # Создаем строку grammar
        self.input_nonterminal = QLineEdit(self)
        self.input_nonterminal.move(20, 90)
        self.input_nonterminal.resize(260, 40)
        
        
        
        self.grammar_lbl = QLabel('Введите регулярную грамматику:', self)
        self.grammar_lbl.move(20,130)
        self.grammar_lbl.resize(260, 20)

        # Создаем строку grammar
        self.input_grammar = QLineEdit(self)
        self.input_grammar.move(20, 150)
        self.input_grammar.resize(260, 40)

        self.choice_lbl = QLabel('Выберите метод:', self)
        self.choice_lbl.move(20,190)
        self.choice_lbl.resize(200, 20)

        self.combo_box = QComboBox(self)
        self.combo_box.addItems(['LL', 'RL'])
        self.combo_box.move(20,210)
        self.combo_box.resize(100, 30)
        
        self.generate_button = QPushButton('Сгенерировать regex', self)
        self.generate_button.move(130,210)
        self.generate_button.resize(150, 30)
        self.generate_button.clicked.connect(self.generate_regex)

        self.regex_lbl = QLabel('Получившееся регулярное выражение:', self)
        self.regex_lbl.move(20,240)
        self.regex_lbl.resize(260, 20)

        self.regular_1 = QPlainTextEdit(self, readOnly=True)
        self.regular_1.move(20,260)
        self.regular_1.resize(260, 40)
        font = QFont()
        font.setPointSize(12)
        self.regular_1.setFont(font)

        self.len_lbl = QLabel('Введите максимальную длину строки:', self)
        self.len_lbl.move(20,300)
        self.len_lbl.resize(260, 20)

        self.input_grammar1 = QLineEdit(self)
        self.input_grammar1.move(20, 320)
        self.input_grammar1.resize(100, 30)
        
        self.generate_str_button = QPushButton('Сгенерировать строки', self)
        self.generate_str_button.move(130,320)
        self.generate_str_button.resize(150, 30)
        self.generate_str_button.clicked.connect(self.generate_strs)

        self.str_lbl = QLabel('Сгенерированные строки:', self)
        self.str_lbl.move(20,350)
        self.str_lbl.resize(260, 20)

        self.regular_generated = QPlainTextEdit(self, readOnly=True)
        self.regular_generated.move(20,370)
        self.regular_generated.resize(260, 260)

        self.grammar_str_lbl = QLabel('Сгенерированные строки по грамматике:', self)
        self.grammar_str_lbl.move(300, 10)
        self.grammar_str_lbl.resize(270, 20)

        self.grammar_regular_generated = QPlainTextEdit(self, readOnly=True)
        self.grammar_regular_generated.move(300,30)
        self.grammar_regular_generated.resize(260, 200)


        self.user_regex_lbl = QLabel('Регулярное выражение пользователя:', self)
        self.user_regex_lbl.move(300,240)
        self.user_regex_lbl.resize(260, 20)

        # Создаем строку grammar
        self.input_user_regex = QLineEdit(self)
        self.input_user_regex.move(300, 260)
        self.input_user_regex.resize(260, 40)

        self.user_len_lbl = QLabel('Введите максимальную длину строки:', self)
        self.user_len_lbl.move(300,300)
        self.user_len_lbl.resize(260, 20)

        self.input_grammar2 = QLineEdit(self)
        self.input_grammar2.move(300, 320)
        self.input_grammar2.resize(100, 30)
        
        self.user_generate_str_button = QPushButton('Сгенерировать строки', self)
        self.user_generate_str_button.move(410,320)
        self.user_generate_str_button.resize(150, 30)
        self.user_generate_str_button.clicked.connect(self.generate_user_strs)

        self.user_str_lbl = QLabel('Сгенерированные строки пользователя:', self)
        self.user_str_lbl.move(300,350)
        self.user_str_lbl.resize(260, 20)

        self.user_regular_generated = QPlainTextEdit(self, readOnly=True)
        self.user_regular_generated.move(300,370)
        self.user_regular_generated.resize(260, 260)

        self.find_differece = QPushButton('Сравнить', self)
        self.find_differece.move(20,635)
        self.find_differece.resize(540, 20)
        self.find_differece.clicked.connect(self.find_diffs)

        self.diff_regular_generated = QPlainTextEdit(self, readOnly=True)
        self.diff_regular_generated.move(20,665)
        self.diff_regular_generated.resize(540, 220)

        self.find_differece = QPushButton('выгрузить грамматику из файла', self)
        self.find_differece.move(20,875)
        self.find_differece.resize(540, 20)
        self.find_differece.clicked.connect(self.upload_grammar)
    
    def generate_regex(self):
        print(self.combo_box.currentText())

        if self.combo_box.currentText() == 'LL':
            choice = 1
        else:
            choice = 2
        self.output_regex = generator(choice, rules=self.input_grammar.text())
        final_regex = "+".join(self.output_regex)
        self.regular_1.setPlainText(final_regex)
        self.input_user_regex.setText(final_regex)
        
    def generate_strs(self):
        self.regular_generated.clear()
        self.grammar_regular_generated.clear()
        self.output_stings = generate_strings("|".join(self.output_regex), int(self.input_grammar1.text()))
        for strings in self.output_stings:
            self.regular_generated.appendPlainText(strings)
        self.input_grammar2.setText(self.input_grammar1.text())
        
        for i in self.input_terminal.text().split():
            if i.isupper():
                raise AttributeError("Все терминальные символы должны быть маленькие")
        for i in self.input_nonterminal.text().split():
            if i.islower():
                raise AttributeError("Все нетерминальные символы должны быть большими")

        # Загрузка грамматики
        vt = self.input_terminal.text().split()
        vn = self.input_nonterminal.text().split()
        p = convert_to_dict(self.input_grammar.text().split())
        s = get_start_symbol(convert_to_dict(self.input_grammar.text().split()))

        # Генерация цепочек
        left_border = 0
        int(self.input_grammar2.text())
        self.output = generate_main(vt,vn,p,s, int(self.input_grammar1.text()))
        for i in self.output_stings:
            if len(i) == 1:
                self.output.append(i)
        if len(set(self.output_stings)-set(self.output))!=0:
            raise ValueError('Ошибка генерации строк')
        else:
            for strings in self.output:
                self.grammar_regular_generated.appendPlainText(strings)
        

    
    def generate_user_strs(self):
        for i in self.input_user_regex.text():
            if i not in self.input_nonterminal.text().split():
                raise AttributeError(f'данного симола нет в нетерминалах {i}')
        self.user_regular_generated.clear()
        user_regex = self.input_user_regex.text().split('+')
        self.output_user_stings = generate_strings("|".join(user_regex), int(self.input_grammar2.text()))
        for strings in self.output_user_stings:
            self.user_regular_generated.appendPlainText(strings)
    
    def find_diffs(self):
        self.diff_regular_generated.clear()
        if len(set(self.output)-set(self.output_user_stings)) == 0:
            self.diff_regular_generated.appendPlainText("All ok")
        else:
            for item in set(self.output)-set(self.output_user_stings):
                if item in self.output:
                    self.diff_regular_generated.appendPlainText(f"{item} -> грамматика")
                else:
                    self.diff_regular_generated.appendPlainText(f"{item} -> пользователь")
    
    def upload_grammar(self):
        vt, vn, p, s= read_json()
        self.input_terminal.setText(vt)
        self.input_nonterminal.setText(vn)
        self.input_grammar.setText(p)

    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())