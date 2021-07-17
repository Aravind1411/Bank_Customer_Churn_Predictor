from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import pandas as pd
import sklearn
import matplotlib
app = Flask(__name__)

df=pd.read_csv(r'C:/Users/Aravind/Downloads/archive/Churn_Modelling.csv')
minage=df['Age'].min()
maxage=df['Age'].max()
minbalratio=0.0
maxbalratio=1326.1027792915531
mintenurebyage=0.0 
maxtenurebyage=0.5555555555555556
mincreditage=4.857142857142857
maxcreditage=46.888888888888886
mincreditscore=df['CreditScore'].min()

maxcreditscore=df['CreditScore'].max()
mintenure=df['Tenure'].min()
maxtenure=df['Tenure'].max()
minbalance=df['Balance'].min()
maxbalance=df['Balance'].max()
minproducts=df['NumOfProducts'].min()

maxproducts=df['NumOfProducts'].max()
minsalary=df['EstimatedSalary'].min()
maxsalary=df['EstimatedSalary'].max()
model = pickle.load(open('Customer_Churn_aravind_final.pkl', 'rb'))
@app.route('/', methods=['GET'])
def Home():
    return render_template('index_1.html')

@app.route('/predict',methods=['POST'])
def predict():
    if request.method == 'POST':
        CreditScore = int(request.form['CreditScore'])
        Age = int(request.form['Age'])
        Tenure = int(request.form['Tenure'])
        Balance = float(request.form['Balance'])
        NumOfProducts = int(request.form['NumOfProducts'])
        HasCrCard = int(request.form['HasCrCard'])
        IsActiveMember = int(request.form['IsActiveMember'])
        EstimatedSalary = float(request.form['EstimatedSalary'])
        Geography_Germany = request.form['Geography_Germany']
        if(Geography_Germany == 'Germany'):
            Geography_Germany = 1
            Geography_Spain= -1
            Geography_France = -1
                
        elif(Geography_Germany == 'Spain'):
            Geography_Germany = -1
            Geography_Spain= 1
            Geography_France = -1
        
        else:
            Geography_Germany = -1
            Geography_Spain= -1
            Geography_France = 1
        Gender= request.form['Gender']
        if(Gender == 'Male'):
            Gender_Male = 1
            Gender_Female = -1
        else:
            Gender_Male = -1
            Gender_Female = 1
        BalanceSalaryRatio= Balance/EstimatedSalary
        TenureByAge	=Tenure/Age
        CreditScoreGivenAge=CreditScore/Age
        new_age=(Age-minage)/(maxage-minage)
        new_credit_score=(CreditScore-mincreditscore)/(maxcreditscore-mincreditscore)
        new_tenure=(Tenure-mintenure)/(maxtenure-mintenure)
        new_balance=(Balance-minbalance)/(maxbalance-minbalance)
        new_no_products=(NumOfProducts-minproducts)/(maxproducts-minproducts)
        new_salary=(EstimatedSalary-minsalary)/(maxsalary-minsalary)
        new_balance_salary_ratio=(BalanceSalaryRatio-minbalratio)/(maxbalratio-minbalratio)
        new_tenure_by_age=(TenureByAge-mintenurebyage)/(maxtenurebyage-mintenurebyage)
        new_credit_score_age=(CreditScoreGivenAge-mincreditage)/(maxcreditage-mincreditage)
        prediction = model.predict([[new_credit_score,new_age,new_tenure,new_balance,new_no_products,HasCrCard,IsActiveMember,new_salary,new_balance_salary_ratio,new_tenure_by_age,new_credit_score_age,Geography_France,Geography_Spain,Geography_Germany,Gender_Female,Gender_Male]])
        
        print(prediction)
        if prediction==1:
             return render_template('index_1.html',prediction_text="The Customer is likely to leave the bank")
        else:
             return render_template('index_1.html',prediction_text="The Customer will not leave the bank")
                
if __name__=="__main__":
    app.run(debug=True)
