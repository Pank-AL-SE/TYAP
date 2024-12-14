from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from gramma import Grammar
import sys
import os
from build_str import Build_str
from create_grammar import Create_grammar

class MainWindow(QMainWindow):
    def __init__(self):
 
        super(MainWindow, self).__init__()
        
        self.grammar = Grammar()
        self.setWindowTitle("lab TYAP")
        self.setGeometry(300,250,700,400)
        self.setFixedSize(1000,400)
        
        self.btn_create_grammar = QtWidgets.QPushButton(self)
        self.btn_create_grammar.setText("Create your own grammar")
        self.btn_create_grammar.move(0,0)
        self.btn_create_grammar.setFixedSize(385,100)
        self.btn_create_grammar.clicked.connect(self.create_grammar)

        self.btn_use_pattern1 = QtWidgets.QPushButton(self)
        self.btn_use_pattern1.setText("Use pattern grammar")
        self.btn_use_pattern1.move(0,100)
        self.btn_use_pattern1.setFixedSize(385,100)
        self.btn_use_pattern1.clicked.connect(self.use_pattern_grammar)

        self.btn_use_func = QtWidgets.QPushButton(self)
        self.btn_use_func.setText("do something")
        self.btn_use_func.move(0,200)
        self.btn_use_func.setFixedSize(385,100)
        self.btn_use_func.clicked.connect(self.create_output)

        self.btn_update_grammar = QtWidgets.QPushButton(self)
        self.btn_update_grammar.setText("Update grammar")
        self.btn_update_grammar.move(0,300)
        self.btn_update_grammar.setFixedSize(385,100)
        self.btn_update_grammar.clicked.connect(self.update_label)


        

        self.lbl = QtWidgets.QLabel(self)
        self.lbl.setText("Grammar\n")
        self.lbl.setFont(QFont('Arial', 30))
        self.lbl.move(390,0)
        self.lbl.setFixedSize(610,400)


    def update_label(self):
        output = 'Grammar\nVT: '
        for i in range(len(self.grammar.VT)):
            output+= self.grammar.VT[i]
            if i!=len(self.grammar.VT)-1:
                output+=', '
        output+='\nVN: '
        for i in range(len(self.grammar.VN)):
            output+= self.grammar.VN[i]
            if i!=len(self.grammar.VN)-1:
                output+=', '
        output+='\nP: '
        for key, value in self.grammar.P.items():
            output+=f'{key}->'
            for i in range(len(value)):
                output+= value[i]
                if i!=len(value)-2:
                    output+='| '
            output+='\n'
        output+='S -> '+ self.grammar.S        
        self.lbl.setText(output)

    def use_pattern_grammar(self):
        self.grammar.simple_grammar()
        self.update_label()
    
    def create_output(self):
        self.mainwindow = Build_str(grammar=self.grammar)
        self.mainwindow.show()
    
    def create_grammar(self):
        self.mainwindow = Create_grammar(grammar=self.grammar)
        self.mainwindow.show()
        

    
    
  
                        

        


    

        




if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    app.exec()
