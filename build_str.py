from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from gramma import Grammar
import gram_func
import sys
import os
class Build_str(QWidget):

    def __init__ (self,grammar): 
        super().__init__()
        self.grammar = grammar
        self.setWindowTitle("Output")
        self.setGeometry(300,250,700,400)
        self.setFixedSize(1000,400)
        
        self.diap_a = QLineEdit(self)
        self.diap_a.move(0, 0)
        self.diap_a.setFixedSize(100,25)
        self.diap_a.setPlaceholderText("from")

        self.diap_b = QLineEdit(self)
        self.diap_b.move(100, 0)
        self.diap_b.setFixedSize(100,25)
        self.diap_b.setPlaceholderText("to")

        self.btn_use = QtWidgets.QPushButton(self)
        self.btn_use.setText("create_str")
        self.btn_use.move(200,0)
        self.btn_use.setFixedSize(100,25)
        self.btn_use.clicked.connect(self.use_func)
        

        self.lbl = QtWidgets.QLabel(self)
        self.lbl.setText("Create\n")
        self.lbl.move(0,25)
        self.lbl.setFixedSize(1000,375)

    def use_func(self):
        left_border = int(self.diap_a.text())
        right_border = int(self.diap_b.text())
        res = gram_func.opration(self.grammar,left_border,right_border)
        output = ''
        for i in res:
            output += f'{i}\n'
        self.lbl.setText(output)




    