import sys
import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('Автомат')
        self.resize(800, 600)
        
        # Центральная область
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        # Виджет списка
        self.list_view = QListWidget()
        self.list_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        # Кнопки и другие элементы управления
        self.load_config_button = QPushButton('Загрузить конфигурацию')
        self.start_button = QPushButton('Начать')
        self.command_line_edit = QLineEdit()
        self.log_text_edit = QPlainTextEdit()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 500)
        
        # Скрытие некоторых элементов
        self.log_text_edit.hide()
        self.start_button.hide()
        self.slider.hide()
        
        # Размещение элементов
        layout = QVBoxLayout()
        layout.addWidget(self.load_config_button)
        layout.addWidget(self.list_view)
        layout.addWidget(self.command_line_edit)
        layout.addWidget(self.start_button)
        layout.addWidget(self.slider)
        layout.addWidget(self.log_text_edit)
        central_widget.setLayout(layout)
        
        # Сигналы и слоты
        self.load_config_button.clicked.connect(self.on_load_config_clicked)
        self.start_button.clicked.connect(self.on_start_clicked)
    
    def parse_json_file(self, file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            self.states = []
            self.alphabet = []
            self.in_stack = []
            self.in_transform = []
            self.transition_function = {}
            self.start_state = None
            self.start_stack = None
            self.end_states = []
            
            if 'states' in data and isinstance(data['states'], list):
                self.states.extend(data['states'])
                print(f'States: {self.states}')
            else:
                print('Массив "states" не найден или не является массивом!')
                return False
            
            if 'alphabet' in data and isinstance(data['alphabet'], list):
                self.alphabet.extend(data['alphabet'])
                if 'ε' not in self.alphabet:
                    self.alphabet.append('ε')
                print(f'Alphabet: {self.alphabet}')
            else:
                print('Массив "alphabet" не найден или не является массивом!')
                return False
            
            if 'in_stack' in data and isinstance(data['in_stack'], list):
                self.in_stack.extend(data['in_stack'])
                print(f'In stack: {self.in_stack}')
            else:
                print('Массив "in_stack" не найден или не является массивом!')
                return False
            
            if 'in_transform' in data and isinstance(data['in_transform'], list):
                self.in_transform.extend(data['in_transform'])
                print(f'In transform: {self.in_transform}')
            else:
                print('Массив "in_transform" не найден или не является массивом!')
                return False
            
            if 'rules' in data and isinstance(data['rules'], list):
                for rule in data['rules']:
                    if len(rule) != 6 or not all(isinstance(x, str) for x in rule):
                        print('Неверный формат правила!')
                        return False
                    
                    key = tuple(rule[:3])
                    value = tuple(rule[3:])
                    self.transition_function[key] = value
                
                print(f'Transition function: {self.transition_function}')
            else:
                print('Массив "rules" не найден или не является массивом!')
                return False
            
            if 'start' in data and isinstance(data['start'], str):
                self.start_state = data['start']
                print(f'Start state: {self.start_state}')
            else:
                print('Значение "start" не найдено или не является строкой!')
                return False
            
            if 'start_stack' in data and isinstance(data['start_stack'], str):
                self.start_stack = data['start_stack']
                print(f'Start stack: {self.start_stack}')
            else:
                print('Значение "start_stack" не найдено или не является строкой!')
                return False
            
            if 'ends' in data and isinstance(data['ends'], list):
                self.end_states.extend(data['ends'])
                print(f'End states: {self.end_states}')
            else:
                print('Массив "ends" не найден или не является массивом!')
                return False
            
            return True
        except FileNotFoundError:
            print(f'Файл {file_path} не найден!')
            return False
        except json.JSONDecodeError as e:
            print(f'Ошибка декодирования JSON: {e}')
            return False
    
    def populate_list(self):
        self.list_view.clear()
        for key, value in self.transition_function.items():
            item_str = f'{key} -> {value}'
            self.list_view.addItem(item_str)
    
    def open_fields(self):
        self.load_config_button.setEnabled(True)
        self.start_button.setEnabled(True)
        self.command_line_edit.setEnabled(True)
    
    def print_stack(self, stack):
        return ''.join(reversed(stack))
    
    def on_start_clicked(self):
        self.load_config_button.setEnabled(False)
        self.start_button.setEnabled(False)
        self.command_line_edit.setEnabled(False)
        self.log_text_edit.clear()
        
        command = self.command_line_edit.text()
        state = self.start_state
        stack = [self.start_stack]
        result_transform = ''
        position = 0
        
        while position < len(command) and stack:
            char = command[position] if position < len(command) else 'ε'
            top_of_stack = stack[-1] if stack else 'ε'

            log_string = f'<font color="green">({state}, {char}, {self.print_stack(stack)})</font>'
            self.log_text_edit.appendHtml(log_string)
            
            if state not in self.states:
                error_string = f'<font color="red">δ({state}, {char}, {top_of_stack}) -> Состояния {{{state}}} не существует!!</font>'
                self.log_text_edit.appendHtml(error_string)
                self.open_fields()
                return
            
            if char not in self.alphabet:
                error_string = f'<font color="red">δ({state}, {char}, {top_of_stack}) -> Символ {{{char}}} не входит в алфавит!</font>'
                self.log_text_edit.appendHtml(error_string)
                self.open_fields()
                return
            
            if top_of_stack not in self.in_stack:
                error_string = f'<font color="red">δ({state}, {char}, {top_of_stack}) -> Символ {{{top_of_stack}}} не входит в алфавит стека!</font>'
                self.log_text_edit.appendHtml(error_string)
                self.open_fields()
                return
            
            search_key = (state, char, top_of_stack)
            if search_key not in self.transition_function:
                error_string = f'<font color="red">Не существует правила перехода ({state}, {char}, {top_of_stack}). Цепочка не принадлежит заданному МП!</font>'
                self.log_text_edit.appendHtml(error_string)
                self.open_fields()
                return
            
            new_state, stack_operation, transform_operation = self.transition_function[search_key]
            
            if len(stack_operation) > 1:
                stack.pop()
                for char in reversed(stack_operation):
                    stack.append(char)
            elif stack_operation == 'ε':
                pass  # Не удалять ничего из стека, так как операция пустая
            else:
                stack.pop()  # Удаляем верхний элемент
                stack.append(stack_operation)  # Добавляем новый элемент
            
            if transform_operation != 'ε':
                result_transform += transform_operation
            
            state = new_state
            position += 1 if char != 'ε' else 0
            
            right_string = f'<font color="green">Новое состояние {{{new_state}}} оставшаяся цепочка - {command[position:]} | Цепочка перевода {{{result_transform}}}</font>'
            self.log_text_edit.appendHtml(right_string)
            self.log_text_edit.appendHtml(f'<font color="green">Стек ({self.print_stack(stack)})</font>')
            
            delay_ms = self.slider.value()
            QThread.msleep(delay_ms)
        
        if position < len(command):
            error_string = f'<font color="red">В цепочке остались символы: {command[position:]}. Цепочка не принадлежит заданному МП!</font>'
            self.log_text_edit.appendHtml(error_string)
            self.open_fields()
            return
        
        if state not in self.end_states:
            error_string = f'<font color="red">Состояние {{{state}}} не является конечным. Цепочка не принадлежит заданному МП!</font>'
            self.log_text_edit.appendHtml(error_string)
            self.open_fields()
            return
        
        self.log_text_edit.appendHtml(f'<font color="green">Перевод цепочки = {result_transform}</font>')
        self.open_fields()
    
    def on_load_config_clicked(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Выбрать файл', '', 'JSON Files (*.json)')
        if file_name:
            success = self.parse_json_file(file_name)
            if success:
                self.populate_list()
                self.log_text_edit.show()
                self.start_button.show()
                self.slider.show()

# Запуск приложения
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())