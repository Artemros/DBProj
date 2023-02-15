from __future__ import annotations
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
import sys
from array import *
import math
from interface.back import ConnectDB
from typing import List, Any
import sqlite3
import mysql.connector


# class MetaData():
#     mydb = mysql.connector.connect(
#         host="localhost",
#         user="meta",
#         password="meta"
#
#     mycursor = mydb.cursor()
#
#     mycursor.execute("SHOW DATABASES")
#
#     for x in mycursor:
#         print(x)


class StartForm(QMainWindow):
    def __init__(self, parent=None):
        super(StartForm, self).__init__(parent)
        # self.sets = Settings(self)
        self.window = QMainWindow(self)
        self.setWindowTitle("DBProj")
        width = 1200
        height = 800
        self.setFixedSize(width, height)
        self.current_page_num = 1
        self.minimumFP = 1
        self.maximumLP = 45
        self.fpButtonPos = QPoint(450, 670)
        self.nextToFPButtonPos = QPoint(50, 0)
        self.listSize = 10

        self.connection = ConnectDB.create_connection("localhost", "root", "root", "LoL")
        self.cursor = self.connection.cursor()
        self.query = "select count(*) from champion"
        self.cursor.execute(self.query)
        self.tableSize = self.cursor.fetchone()[0]
        self.maximumLP = math.ceil(self.tableSize / self.listSize)
        self.query = """select * from champion limit %s offset %s"""

        # self.cursor.execute(self.query)
        # self.result = self.cursor.fetchall()
        # self.result: List[Any] = list(self.cursor.fetchall())
        # Adding DB Button
        # self.DBButton = QPushButton("Disconnect DB", self)
        # self.DBButton.setFixedSize(100, 30)
        # self.DBButton.move(1000, 770)
        # self.DBButton.clicked.connect(self.disconnect_db)
        # Settings Button
        # self.layout = QGridLayout()
        # self.setLayout(self.layout)
        # self.settingsButton = QPushButton("Settings", self)
        # self.settingsButton.setFixedSize(100, 30)
        # self.settingsButton.move(1100, 50)
        #
        # self.settingsButton.clicked.connect(self.open_settings)
        # self.dialog = Settings(self)
        # Exit Button
        self.exitButton = QPushButton("Exit", self)
        self.exitButton.setFixedSize(100, 30)
        self.exitButton.move(1100, 770)
        self.exitButton.clicked.connect(self.close_program)
        # Save Button

        self.num = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        self.entPP = QComboBox(self)
        for n in self.num:
            self.entPP.addItem(n)

        self.entPP.move(1100, 60)
        self.entPP.currentTextChanged.connect(self.on_combobox_change)

        self.entPPLabel = QLabel("Entity per page:", self)
        self.entPPLabel.move(1100, 30)

        self.thing = int(self.entPP.currentText())
        self.listSize = self.thing
        # self.saveButton = QPushButton("Save", self)
        # self.saveButton.setFixedSize(100, 30)
        # self.saveButton.move(1100, 150)
        # self.saveButton.clicked.connect(self.save_settings)
        # Go To First Page
        self.fpButton = QPushButton("⇐", self)
        self.fpButton.setFixedSize(30, 30)
        self.fpButton.move(self.fpButtonPos)
        self.fpButton.clicked.connect(self.go_to_first_page)
        # Go To Last Page
        self.lpButton = QPushButton("⇒", self)
        self.lpButton.setFixedSize(30, 30)
        self.lpButton.move(self.fpButtonPos + self.nextToFPButtonPos * 4)
        self.lpButton.clicked.connect(self.go_to_last_page)
        # Go To Previous Page
        self.ppButton = QPushButton("←", self)
        self.ppButton.setFixedSize(30, 30)
        self.ppButton.move(self.fpButtonPos + self.nextToFPButtonPos)
        self.ppButton.clicked.connect(self.go_to_previous_page)
        # Go To Next Page
        self.npButton = QPushButton("→", self)
        self.npButton.setFixedSize(30, 30)
        self.npButton.move(self.fpButtonPos + self.nextToFPButtonPos * 3)
        self.npButton.clicked.connect(self.go_to_next_page)
        # Current Page
        self.currentPage = QLabel("1", self)
        self.currentPage.setFixedSize(30, 30)
        self.currentPage.move(self.fpButtonPos + self.nextToFPButtonPos * 2)
        self.currentPage.setText(str(self.current_page_num))

        # Table for DB
        self.dbTable = QTableWidget(self)
        self.dbTable.setRowCount(0)
        self.dbTable.setColumnCount(0)
        self.dbTable.setFixedSize(900, 500)
        self.dbTable.move(150, 100)
        self.show_actual_data()
        # self.setCentralWidget(self.dbTable)
        # self.dbTable.show()
        # Adding Widgets on layout
        # self.layout.addWidget(self.settingsButton)
        # self.layout.addWidget(self.exitButton)

    # def open_settings(self):
    #     self.sets.show()

    def save_settings(self):
        self.listSize = self.thing

    def on_combobox_change(self):
        self.listSize = int(self.entPP.currentText())
        self.show_actual_data()
        self.maximumLP = math.ceil(self.tableSize / self.listSize)

    def close_program(self):
        self.close()

    # def change_list_size(smth):
    #     StartForm.listSize = smth

    def disconnect_db(self):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        print("disconnected from DB")

    def show_actual_data(self):
        self.dbTable.clear()
        self.dbTable.setRowCount(0)
        self.dbTable.setColumnCount(2)
        tuple1 = (self.listSize, (self.current_page_num - 1) * self.listSize)
        self.cursor.execute(self.query, tuple1)
        result = self.cursor.fetchall()
        for row_number, row_data in enumerate(result):
            self.dbTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.dbTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def go_to_first_page(self):
        self.current_page_num = self.minimumFP
        # print(self.current_page_num)
        self.currentPage.setText(str(self.current_page_num))
        self.show_actual_data()

    def go_to_previous_page(self):
        if self.current_page_num > self.minimumFP:
            self.current_page_num -= 1
            # print(self.current_page_num)
        else:
            self.current_page_num = self.minimumFP
            # print(self.current_page_num)
        self.currentPage.setText(str(self.current_page_num))
        self.show_actual_data()

    def go_to_next_page(self):
        if self.current_page_num < self.maximumLP:
            self.current_page_num += 1
            # print(self.current_page_num)
        else:
            self.current_page_num = self.maximumLP
            # print(self.current_page_num)
        self.currentPage.setText(str(self.current_page_num))
        self.show_actual_data()

    def go_to_last_page(self):
        self.current_page_num = self.maximumLP
        # print(self.current_page_num)
        self.currentPage.setText(str(self.current_page_num))
        self.show_actual_data()

# class Settings(QMainWindow):
#     def __init__(self, parent=StartForm):
#         super(Settings, self).__init__(parent)
#         self.setWindowTitle("Settings")
#         width = 300
#         height = 300
#         self.setFixedSize(width, height)
#
#         self.layout = QGridLayout()
#
#         self.num = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
#         self.entPP = QComboBox(self)
#         for n in self.num:
#             self.entPP.addItem(n)
#
#         self.entPP.move(90, 60)
#
#         self.entPPLabel = QLabel("Entity per page:", self)
#         self.entPPLabel.move(90, 30)
#         # Save Button
#         self.saveButton = QPushButton("Save", self)
#         self.saveButton.setFixedSize(100, 30)
#         self.saveButton.move(90, 150)
#         self.thing = int(self.entPP.currentText())
#         # self.saveButton.clicked.connect(save_sett())
#         # print(listSize)
#
#     def save_sett(self):
#         change_list_s(3)
