from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from datetime import date
import sys
import mysql.connector

MainUi, _ = loadUiType('shop.ui')


class TailorShop(QMainWindow, MainUi):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.show()
        try:
            self.mydb = mysql.connector.connect(
                host="localhost",
                port="3306",
                user="root",
                password="",
                database="python",
                auth_plugin='mysql_native_password',
            )
            self.db = self.mydb.cursor()
            self.db.execute("use python")
            self.mydb.commit()
        except Exception as f:
            print(f)
            sys.exit()
        self.customer_search.clicked.connect(self.customersearch)
        self.btn_Customer.clicked.connect(self.btn_newCustomer)
        self.finalDate()
        self.loadCustomers()

    def loadCustomers(self):
        self.db.execute(
            "select customer.customer_name ,customer.fabric_type, customer.shoulder_size, customer.waist_size , "
            "customer.hip_size , customer.clothes_categories ,customer.clothes_model , customer.target_date  from "
            "customer ")
        data = self.db.fetchall()
        for d in data:
            row = self.customertable.rowCount()
            self.customertable.insertRow(row)
            self.customertable.setRowCount(row + 1)
            self.customertable.setItem(row, 0, QTableWidgetItem(str(d[0])))
            self.customertable.setItem(row, 1, QTableWidgetItem(str(d[1])))
            self.customertable.setItem(row, 2, QTableWidgetItem(str(d[2])))
            self.customertable.setItem(row, 3, QTableWidgetItem(str(d[3])))
            self.customertable.setItem(row, 4, QTableWidgetItem(str(d[4])))
            self.customertable.setItem(row, 5, QTableWidgetItem(str(d[5])))
            self.customertable.setItem(row, 6, QTableWidgetItem(str(d[6])))
            self.customertable.setItem(row, 7, QTableWidgetItem(str(d[7])))

    def btn_newCustomer(self):
        customer_name = self.customer_name.text()
        fabric_type = self.fabric_type.text()
        shoulder_size = int(self.shoulder_size.text())
        waist_size = int(self.waist_size.text())
        hip_size = int(self.hip_size.text())
        clothes_categories = self.clothes_categories.currentText()
        clothes_model = self.clothes_model.currentText()
        target_date = self.target_date.text()

        self.db.execute(
            "insert into customer (customer_name,fabric_type,shoulder_size,waist_size,hip_size,clothes_categories,"
            "clothes_model,target_date) values (%s,%s,%s,%s,%s,%s,%s,%s);",
            (customer_name, fabric_type, shoulder_size, waist_size, hip_size, clothes_categories, clothes_model,
             target_date))
        self.mydb.commit()

        self.db.execute(
            "select customer.customer_name ,customer.fabric_type, customer.shoulder_size, customer.waist_size , "
            "customer.hip_size , customer.clothes_categories ,customer.clothes_model , customer.target_date  from "
            "customer ")
        data = self.db.fetchall()
        self.customertable.setRowCount(0)
        for d in data:
            row = self.customertable.rowCount()
            self.customertable.insertRow(row)
            self.customertable.setRowCount(row + 1)
            self.customertable.setItem(row, 0, QTableWidgetItem(str(d[0])))
            self.customertable.setItem(row, 1, QTableWidgetItem(str(d[1])))
            self.customertable.setItem(row, 2, QTableWidgetItem(str(d[2])))
            self.customertable.setItem(row, 3, QTableWidgetItem(str(d[3])))
            self.customertable.setItem(row, 4, QTableWidgetItem(str(d[4])))
            self.customertable.setItem(row, 5, QTableWidgetItem(str(d[5])))
            self.customertable.setItem(row, 6, QTableWidgetItem(str(d[6])))
            self.customertable.setItem(row, 7, QTableWidgetItem(str(d[7])))

    def customersearch(self):
        name = self.customer_n.text()
        self.db.execute(
            "select  customer.shoulder_size,customer.waist_size,customer.hip_size from customer "
            "where customer.customer_name = %s", (name,))
        data = self.db.fetchall()

        self.measurementstable.setRowCount(0)
        for d in data:
            row = self.measurementstable.rowCount()
            self.measurementstable.insertRow(row)
            self.measurementstable.setRowCount(row + 1)
            self.measurementstable.setItem(row, 0, QTableWidgetItem(str(d[0])))
            self.measurementstable.setItem(row, 1, QTableWidgetItem(str(d[1])))
            self.measurementstable.setItem(row, 2, QTableWidgetItem(str(d[2])))

    def finalDate(self):
        self.db.execute("select  customer.target_date from customer ")
        data = self.db.fetchall()
        li = []

        for i in range(len(data)):
            li.append(data[i][0])

        today = date.today()
        d3 = today.strftime("%m/%d/%y")
        d = d3.split("/")
        array_length = len(li)
        m = []
        for i in range(array_length):
            m.append(li[i].split("/"))

        array_length3 = len(m)

        for i in range(array_length3):
            month = int(d[0]) == int(m[i][0])
            day = int(d[1]) + 2 == int(m[i][1])
            if month and day:
                self.notifytable.setRowCount(0)
                row = self.notifytable.rowCount()
                self.notifytable.insertRow(row)
                self.notifytable.setRowCount(row + 1)
                self.notifytable.setItem(row, 0, QTableWidgetItem('/'.join(m[i])))

    def __del__(self):
        self.db.close()
        self.mydb.close()


app = QApplication(sys.argv)
window = TailorShop()
app.exec_()
