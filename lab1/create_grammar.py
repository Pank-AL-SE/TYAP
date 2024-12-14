from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from gramma import Grammar
import gram_func
import sys
import os

class Create_grammar(QWidget):

    def __init__ (self,grammar): 
        super().__init__()
        self.grammar = grammar
        self.setWindowTitle("Input Grammar")
        self.setGeometry(300,250,700,400)
        self.setFixedSize(1000,400)
        
        self.input_VT = QLineEdit(self)
        self.input_VT.move(0, 0)
        self.input_VT.setFixedSize(100,25)
        self.input_VT.setPlaceholderText("Input (splited spaces) VT")

        self.input_VN = QLineEdit(self)
        self.input_VN.move(100, 0)
        self.input_VN.setFixedSize(100,25)
        self.input_VN.setPlaceholderText("Input (splited spaces) VN")

        self.btn_use = QtWidgets.QPushButton(self)
        self.btn_use.setText("Update")
        self.btn_use.move(200,0)
        self.btn_use.setFixedSize(100,25)
        self.btn_use.clicked.connect(self.use_func)

    def use_func(self):
        self.mass_input = []
        self.mass_label = []
        self.grammar.VN = list(map(str, self.input_VN.text().split()))
        self.grammar.VT = list(map(str, self.input_VT.text().split()))
        for i in range(len(self.grammar.VN)):
            self.mass_input.append(QLineEdit(self))
            self.mass_input[i].move(20,i*25+50)            
            self.mass_input[i].setFixedSize(100,25)
            self.mass_label.append(QtWidgets.QLabel(self))
            self.mass_label[i].setText(self.grammar.VN[i]+":")
            self.mass_label[i].move(0,i*25+50)
            self.mass_label[i].setFixedSize(20,25)
            self.mass_input[i].show()
            self.mass_label[i].show()

        self.main_S = QLineEdit(self)
        self.main_S.move(320,0)            
        self.main_S.setFixedSize(100,25)
        self.main_S.show()
        self.main_S.setPlaceholderText("S:")

        self.btn_create = QtWidgets.QPushButton(self)
        self.btn_create.setText("Create")
        self.btn_create.move(420,0)
        self.btn_create.setFixedSize(100,25)
        self.btn_create.clicked.connect(self.save_grammar)
        self.btn_create.show()



    def save_grammar(self):
        print(self.grammar.VT)
        print(self.grammar.VN)
        self.grammar.S = str(self.main_S.text())
        print(self.grammar.S)
        self.grammar.P = {}
        for i in range(len(self.grammar.VN)):
            self.grammar.P.update({self.grammar.VN[i]:list(map(str,self.mass_input[i].text().split()))})
            for i in self.grammar.P.values():
                if 'l'in i:
                    i[i.index('l')] = ""
        print(self.grammar.P)

   