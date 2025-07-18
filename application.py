import pickle
from flask import Flask,request,jsonify,render_template
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import logging
logging.basicConfig(level=logging.DEBUG)


application = Flask(__name__)
app = application

### import ridge regressor and standard scalar pickle
ridge_model = pickle.load(open('models/ridge.pkl', 'rb'))
standard_scaler = pickle.load(open('models/scaler.pkl', 'rb'))

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/predictdata",methods=['GET','POST'])
def predict_datapoint():
    if request.method=="POST":
        Temperature=float(request.form.get('Temperature',0))
        RH=float(request.form.get('RH',0))
        Ws=float(request.form.get('Ws',0))
        Rain=float(request.form.get('Rain',0))
        FFMC=float(request.form.get('FFMC',0))
        DMC=float(request.form.get('DMC',0))
        ISI=float(request.form.get('ISI',0))
        Classes=float(request.form.get('Classes',0))
        Region=float(request.form.get('Region',0))

        new_data_scaled = standard_scaler.transform([[Temperature,RH,Ws,Rain,FFMC,DMC,ISI,Classes,Region]])
        result=ridge_model.predict(new_data_scaled)
        return render_template('home.html',results=result[0])



    else:
        return render_template("home.html")
    


if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)