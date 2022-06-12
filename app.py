# from crypt import methods
import csv
from flask import Flask, make_response, redirect, render_template, request,url_for
import pandas as pd
import numpy as np 

import pickle 
import requests



app = Flask(__name__)
model = pickle.load(open('model11.pkl','rb'))


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'

# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), nullable=False, unique=True)
#     password = db.Column(db.String(80), nullable=False)



@app.route('/')
def home():
    # return "HELLO BOIE"
    return render_template('form.html')

@app.route('/predict101/',methods=['POST'])
def predict101():
    print("reached here----")

 
    intfeatures = [str(x) for x in request.form.values()]
    fme=request.form["entry.1247781192"]
    age=request.form["entry.124778119"]
    gender= intfeatures[2]
    if gender =='MALE':
        male=1
        female=0
        pns=0
        intfeatures.append(male)
        intfeatures.append(female)
        intfeatures.append(pns)
    elif gender =='FEMALE':
        male=0
        female=1
        pns=0
        intfeatures.append(male)
        intfeatures.append(female)
        intfeatures.append(pns)
    elif gender =="Prefer not to say":
        male=0
        female=0
        pns=1
        intfeatures.append(male)
        intfeatures.append(female)
        intfeatures.append(pns)
    # del intfeatures[26]
    del intfeatures[2]
    # print(intfeatures)
    del intfeatures[1]
    intfeatures.append(age)
    del intfeatures[0]
    del intfeatures[2]
    
    print(len(intfeatures))
 


    v = []
    for i in intfeatures:
        if (i =="Most of the Time"):v.append(int(7))
        elif(i=="Quite Often"):v.append(int(3))
        elif(i=="Sometimes"):v.append(int(-1))
        elif(i=="Never"):v.append(int(-3))
        elif(i=="No workout"):v.append(int(5))
        elif(i=="10-15"):v.append(int(-11))
        elif(i=="60+ mins"):v.append(int(-6))
        elif(i=="30-60 mins"):v.append(int(-6))
        elif(i=="10-15 mins"):v.append(int(-1))
        elif(i=="Most of the Time/Always"):v.append(int(7))
        elif(i=="Yes"):v.append(int(10))
        elif(i=="No"):v.append(int(-2))
        elif(i=="Prefer not to say"):v.append(int(2))
        else:
            v.append(int(i))
    print(len(v))

    finalfeatures = [np.array(v)]


    prediction = model.predict(finalfeatures)

    output = prediction[0]
    ans_res=" "
    if output == -1:
        ans_res = f"Thanks for your response. Your anxiety levels for today would be slightly less than normal "
    elif output == -5:
        ans_res = f"Thanks for your response. Your anxiety levels for today would be almost zero "
    elif output == 3:
        ans_res = f"Thanks for your response. Your anxiety levels for today would be above normal "
    elif output == 7:
        ans_res = f"Thanks for your response. Your anxiety levels for today very high"

    print(type(output))


    
    return render_template('prediction.html', prediction_text=f'{fme} ,{ans_res} ')






if __name__ == "__main__":
    app.run(debug=True)

