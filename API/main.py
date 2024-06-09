from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import pickle


app = Flask(__name__)





def Prediction(data):
    with open('../dashboard_deploy/ressources/best_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)

    pred_class = model.predict(data)[0]
    pred_proba = np.round(model.predict_proba(data)[0][1]*100, 0)
    if pred_class==1:
        pred_class = "Will Exit"
    else:
        pred_class = "Won't Exit"
    return pred_class, pred_proba


@app.route('/', methods=['GET','POST'])
def dashboard():
    # Importation données
    df = pd.read_csv("./ressources/train.csv")
    df = df.drop(['id', 'CustomerId', 'Surname'], axis = 1)
    # Nombre de clients, nb_actifs, age moyen
    nb_clients = df[df.Exited==0].shape[0]
    nb_actifs = df[df.IsActiveMember==1].shape[0]
    age_moyen = df[df.Exited==0]['Age'].mean().round(1)
    pct_exited = round(df[df.Exited==1].shape[0]/df.shape[0]*100, 1)
    # Graphiques Age
    df['Age_group'] = df['Age'].apply(lambda x : '0-20' if x<=20 else
                                              ('21-30' if x<=30 else
                                                ('31-40' if x<=40 else
                                                ('41-50' if x<=50 else 
                                                 ('51-60' if x<=60 else '60 +'
                                              ) ))))

    df_age = df[['Age_group']].value_counts().reset_index().sort_values(by = 'Age_group')
    age_group = df_age['Age_group'].tolist()
    age_count = df_age['count'].tolist()
    # Graphique Lieu de résidence
    df_geography = df['Geography'].value_counts().reset_index()
    geo_group = df_geography['Geography'].tolist()
    geo_count = df_geography['count'].tolist()
    # Graphique Nombre de produits
    df_prod = df['NumOfProducts'].value_counts().reset_index().sort_values(by = 'NumOfProducts')
    prod_group = df_prod['NumOfProducts'].tolist()
    prod_count = df_prod['count'].tolist()
    # Graphique Sexe
    df_sexe = df['Gender'].value_counts().reset_index()
    sexe_group = df_sexe['Gender'].tolist()
    sexe_count = df_sexe['count'].tolist()
    # Graphique Années banques
    df['tenure_group'] = df['Tenure'].apply(lambda x: '0-2' if x<=2 else
                                       ('3-5' if x<=5 else
                                       ('6-8' if x<=8 else
                                       ('9-11' if x<=11 else '12 +'))))

    df_tenure = df['tenure_group'].value_counts().reset_index().sort_values(by = 'tenure_group')
    tenure_group = df_tenure['tenure_group'].tolist()
    tenure_count = df_tenure['count'].tolist()
    # Graphique Exited
    df_exited = df['Exited'].value_counts().reset_index()
    df_exited['Exited'] = df_exited['Exited'].apply(lambda x: 'Exited' if x==1 else "didn't Exit")
    exited_group = df_exited['Exited'].tolist()
    exited_count = df_exited['count'].tolist()

    del df, df_age, df_geography, df_prod, df_sexe, df_tenure, df_exited

    return render_template("dashboard.html", nb_clients=nb_clients, nb_actifs=nb_actifs, age_moyen=age_moyen,
                           pct_exited = pct_exited, age_group = age_group, age_count = age_count,
                           geo_group=geo_group, geo_count=geo_count, prod_group=prod_group, prod_count=prod_count,
                           sexe_group=sexe_group, sexe_count=sexe_count, tenure_group=tenure_group, tenure_count=tenure_count,
                           exited_group=exited_group, exited_count=exited_count)

@app.route('/prediction',methods=['GET','POST'])
def prediction():
    pred_class = ''
    pred_proba = ''
    if request.method=='POST':
        Age = request.form['Age']
        Gender = request.form['Gender']
        Geography = request.form['Geography']
        HasCrCard = request.form['HasCrCard']
        Balance = request.form['Balance']
        IsActiveMember = request.form['IsActiveMember']
        NumOfProducts = request.form['NumOfProducts']
        CreditScore = request.form['CreditScore']
        Tenure = request.form['Tenure']
        EstimatedSalary = request.form['EstimatedSalary']

        data = pd.DataFrame({'CreditScore':CreditScore, 'Geography':Geography, 'Gender':Gender,
                             'Age':Age, 'Tenure':Tenure, 'Balance':Balance, 'NumOfProducts':NumOfProducts,
                             'HasCrCard':HasCrCard, 'IsActiveMember':IsActiveMember, 'EstimatedSalary':EstimatedSalary},
                             index = [0])

        predictions = Prediction(data)
        pred_class = predictions[0]
        pred_proba = predictions[1]

    return render_template('prediction.html', pred_class=pred_class, pred_proba = pred_proba)

@app.route('/historique',methods=['GET','POST'])
def historique():

    return render_template("tables.html")


if __name__ == "__main__":
    app.secret_key='secret123'
    app.run(debug=True)