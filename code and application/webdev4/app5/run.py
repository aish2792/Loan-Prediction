from flask import Flask, render_template, send_file, g, request, jsonify
import os
from db import Database
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
import pandas as pd
from sklearn.model_selection import train_test_split

app = Flask(__name__, static_folder='public', static_url_path='')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = Database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/course/<path:path>')
def base_static(path):
    return send_file(os.path.join(app.root_path, '..', '..', 'course', path))


@app.route('/api/delete_user')
def delete_user():
    get_db().delete_user()
    return render_template('prediction.html')


def add(dict, key, value):
    dict[key] = value

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/prediction')
def prediction():
    return render_template('prediction.html')

def KFolds(X, y):
    """ Stratified 5 folds, shuffle each stratification of the data before splitting into batches """

    mean_accuracy = []
    i = 1
    kf = StratifiedKFold(n_splits=5, random_state=1, shuffle=True)
    accuracy = 0

    for train_index, test_index in kf.split(X, y):
        # print('\n{} of kfold {}'.format(i, kf.n_splits))
        xtr, xvl = X.loc[train_index], X.loc[test_index]
        ytr, yvl = y[train_index], y[test_index]

        model = LogisticRegression(random_state=1)
        model.fit(xtr, ytr)
        pred_test = model.predict(xvl)
        score = accuracy_score(yvl, pred_test)
        mean_accuracy.append(score)
        i += 1

    accuracy =  sum(mean_accuracy) / len(mean_accuracy)
    return accuracy

@app.route('/create_userDetails', methods=['GET', 'POST'])
def create_userDetails():
    user_data = {}
    test = []
    X = pd.read_csv("X_train.csv")
    Y = pd.read_csv("Y_train.csv")
    X = X.iloc[:, 1:]
    y = Y.iloc[:, 1]
    firstName = ""

    updated = {'Credit_History': 0, 'Total_Income': 0, 'Gender_Female': 0, 'Gender_Male': 0,
               'Married_No': 0, 'Married_Yes': 0, 'Dependents_3': 0,
               'Dependents_2': 0, 'Dependents_1': 0, 'Dependents_0': 0, 'Education_Graduate': 0,
               'Education_Not Graduate': 0, 'Self_Employed_No': 0, 'Self_Employed_Yes': 0, 'Property_Area_Rural': 0,
               'Property_Area_Semiurban': 0, 'Property_Area_Urban': 0, 'EMI': 0, 'Balance Income': 0}


    """ Split the data into train and cross validation set """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    """ Make prediction """
    predictions = model.predict(X_test)

    """ Accuracy """
    score = model.score(X_test, y_test)

    """ KFolds """
    k = KFolds(X, y)
    
    
    if request.method == 'POST':

        gender = request.form['gender']
        if gender == 'Female':
            gender = 0
        else:
            gender = 1
        add(user_data, 'gender', gender)

        fname = request.form['fname']
        fname = fname.capitalize()
        firstName = fname
        add(user_data, 'fname', fname)

        lname = request.form['lname']
        lname = lname.capitalize()
        add(user_data, 'lname', lname)

        marr = request.form['marr']
        add(user_data, 'marr', marr)

        dependents = request.form['dependents']
        add(user_data, 'dependents', dependents)

        edu = request.form['edu']
        add(user_data, 'edu', edu)

        emp = request.form['emp']
        add(user_data, 'emp', emp)

        appIncome = request.form['appIncome']
        add(user_data, 'appIncome', appIncome)

        coIncome = request.form['coIncome']
        add(user_data, 'coIncome', coIncome)

        loanAmt = request.form['loanAmt']
        add(user_data, 'loanAmt', loanAmt)

        loanAmtTerm = request.form['loanAmtTerm']
        loanAmtTerm = float(loanAmtTerm) * 365
        add(user_data, 'loanAmtTerm', loanAmtTerm)

        creditHistory = request.form['creditHistory']
        if creditHistory > '650':
            creditHistory = 1
        else:
            creditHistory = 0

        add(user_data, 'creditHistory', creditHistory)


        property = request.form['property']
        property = property.capitalize()
        add(user_data, 'property', property)

    
    get_db().create_profile(user_data)
    test_list = get_db().select_profile()
    dfObj = pd.DataFrame(test_list)


    EMI = float(dfObj['EMI'].values)
    updated['EMI'] = EMI

    cred_score = float(dfObj['Credit_History'].values)
    updated['Credit_History'] = cred_score

    total_income = float(dfObj['App_Income']) + float(dfObj['coApp_Income'])
    updated['Total_Income'] = total_income

    bal_income = total_income - EMI*1000
    updated['Balance Income'] = bal_income

    if dfObj['Gender'].values == 'Female':
        updated['Gender_Female'] = 1
        updated['Gender_Male'] = 0

    else:
        updated['Gender_Female'] = 0
        updated['Gender_Male'] = 1

    if dfObj['Married'].values == 'Yes':
        updated['Married_No'] = 0
        updated['Married_Yes'] = 1

    else:
        updated['Married_No'] = 1
        updated['Married_Yes'] = 0

    if dfObj['Dependents'].values == 0:
        updated['Dependents_0'] = 1
        updated['Dependents_1'] = 0
        updated['Dependents_2'] = 0
        updated['Dependents_3'] = 0

    elif dfObj['Dependents'].values == 1:
        updated['Dependents_0'] = 0
        updated['Dependents_1'] = 1
        updated['Dependents_2'] = 0
        updated['Dependents_3'] = 0

    elif dfObj['Dependents'].values == 2:
        updated['Dependents_0'] = 0
        updated['Dependents_1'] = 0
        updated['Dependents_2'] = 1
        updated['Dependents_3'] = 0

    else:
        updated['Dependents_0'] = 0
        updated['Dependents_1'] = 0
        updated['Dependents_2'] = 0
        updated['Dependents_3'] = 1

    if dfObj['Education'].values == 'Graduate':
        updated['Education_Graduate'] = 1
        updated['Education_Not Graduate'] = 0

    else:
        updated['Education_Graduate'] = 0
        updated['Education_Not Graduate'] = 1

    if dfObj['Self_Employed'].values == 'Yes':
        updated['Self_Employed_Yes'] = 1
        updated['Self_Employed_No'] = 0

    else:
        updated['Self_Employed_Yes'] = 0
        updated['Self_Employed_No'] = 1

    if dfObj['Property_Area'].values == 'Urban':
        updated['Property_Area_Rural'] = 0
        updated['Property_Area_Semiurban'] = 0
        updated['Property_Area_Urban'] = 1

    elif dfObj['Property_Area'].values == 'Semiurban':
        updated['Property_Area_Rural'] = 0
        updated['Property_Area_Semiurban'] = 1
        updated['Property_Area_Urban'] = 0

    else:
        updated['Property_Area_Rural'] = 1
        updated['Property_Area_Semiurban'] = 0
        updated['Property_Area_Urban'] = 0


    test = pd.DataFrame(updated, index=[0])
    pred_test = model.predict(test)
    if pred_test == 1:
        return render_template('thankyou.html', firstName=firstName)
    else:
        return render_template('noThankyou.html', firstName=firstName)

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/noThankyou')
def noThankyou():
    return render_template('noThankyou.html')



if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)


