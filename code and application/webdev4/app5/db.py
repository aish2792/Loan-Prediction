import os
import sqlite3
import collections

SQLITE_PATH = os.path.join(os.path.dirname(__file__), 'loanPrediction.db')


class Database:

    def __init__(self):
        self.conn = sqlite3.connect(SQLITE_PATH)


    def select(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        return c.fetchall()


    def execute(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        self.conn.commit()


    def delete_user(self):
        """ Delete the user selection of userinfo in the "ingredients" table """

        self.execute('DELETE FROM userInfo')


    def create_profile(self, name):
        """ Takes form input from the user and stores it in the database """

        a = float(name['loanAmt'])
        b = float(name['loanAmtTerm'])
        name['EMI'] = a/b

        self.execute('INSERT INTO userInfo (firstName, lastName, gender, maritalStatus, dependents, education, selfEmp, appIncome, coIncome, loanAmt, loanAmtTerm, creditHistory, property, EMI)'
                     ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',[name['fname'], name['lname'], name['gender'], name['marr'], name['dependents'], name['edu'], name['emp'], name['appIncome'], name['coIncome'], a, b, name['creditHistory'], name['property'],name['EMI'] ])

    def select_profile(self):
        data = self.select('SELECT * FROM userInfo')
        return [{
            'Gender': d[2],
            'Married': d[3],
            'Dependents': d[4],
            'Education': d[5],
            'Self_Employed': d[6],
            'App_Income': d[7],
            'coApp_Income': d[8],
            'LoanAmount': d[9],
            'Loan_Amount_Term': d[10],
            'Credit_History': d[11],
            'Property_Area': d[12],
            'EMI' : d[13]
        } for d in data]



    def close(self):
        self.conn.close()




