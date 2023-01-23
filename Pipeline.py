
from flask import Blueprint,request, jsonify,render_template
import traceback
import numpy as np
import pandas as pd 
import os
from sklearn.ensemble import RandomForestClassifier
import joblib
from sklearn.preprocessing import MinMaxScaler


view= Blueprint(__name__,"views")

@view.route('/', methods=['GET'])
def Page():
    if request.method == "GET":

        with open (r"templates\result.html","w") as htmlR:
                htmlR=htmlR.truncate()
        with open (r"templates\resultRecap.html") as htmlR:
                htmlR=htmlR.read()
        with open (r"templates\result.html","w") as htmlW:
                htmlW.write(htmlR)
   
        return render_template('Home.html')

####################################################################

@view.route('/predict',methods=['GET'])
def Predict():
    if request.method == "GET":

        with open (r"templates\result.html","w") as htmlR:
                htmlR=htmlR.truncate()
        with open (r"templates\resultRecap.html") as htmlR:
                htmlR=htmlR.read()
        with open (r"templates\result.html","w") as htmlW:
                htmlW.write(htmlR)
             
        return render_template('predict.html')

####################################################################

@view.route('/result', methods=['POST','GET'])
def Result():
    res=[]
    if request.method == "POST":
        try:    

                    ################## deserialization of the model ####
                    model = joblib.load("MyMachine.pkl") 
                    print ('Model loaded',model)

                    model_columns = joblib.load("model_columns_11.pkl") 
                    
                    print ('Model columns loaded')

                    ################### Receiving ######################
                    file= request.files["dataplayer"]
                    file.save(os.path.join("Uploads",file.filename))
                    file.name
                    print("Data recived")

                    df=pd.read_excel("Uploads/"+file.filename)
                    df.fillna(value=0.0)
                    Col_set = df['Name'].values.tolist()
                    df_val= df.drop(['Name'],axis=1).values
                    
                    ############### Transformation#########################
                    for x in np.argwhere(np.isnan(df_val)):
                        df_val[x]=0.0
                    Norma_set=MinMaxScaler().fit_transform(df_val)
                    
                    ################ Prediction ###########################

                    prediction = list(model.predict(Norma_set))  
                     
                    ################## Loading result to new DataFrame#######
                    dplayer = pd.DataFrame ([Col_set,prediction]).transpose()
                    dplayer.columns=['Name_player','Preduction'] 
                    dplayer['comment']=" "
                    for i in range(len(dplayer)):
                        if dplayer['Preduction'][i]==1.0:
                            dplayer['comment'][i]="Most likely is a good player"
                        else :
                            dplayer['comment'][i]="Most likely is a bad player"
                    
                    
                    ################## Display Result on HTML page############
                    
                    res=dplayer.to_html()

                    ##########################################################
                    
                    with open (r"templates\result.html") as htmlR:
                         htmlR=htmlR.read()
                    htmlR=htmlR.replace('<table>',res)

                    with open (r"templates\result.html","w") as htmlW:
                         htmlW.write(htmlR)
                    
                    #os.remove("Uploads/"+file.filename)
                    return render_template('result.html',result=res)

                   
                    

        except:

                return jsonify({'trace': traceback.format_exc()})
            
                
    if request.method == "GET":
        
        with open (r"templates\result.html","w") as htmlR:
                htmlR=htmlR.truncate()
        with open (r"templates\resultRecap.html") as htmlR:
                htmlR=htmlR.read()
        with open (r"templates\result.html","w") as htmlW:
                htmlW.write(htmlR)
        
             
        return render_template('resultLite.html')

    




