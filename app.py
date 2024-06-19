from flask import Flask,render_template,request,redirect, url_for,session
import pandas as pd
import pickle
from sklearn.tree import DecisionTreeClassifier
import joblib
import numpy as np
import sqlite3


app = Flask(__name__)
app.secret_key = "secret"


@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    r = ""
    msg = ""
    if(request.method == "POST"):
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect("register.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = '"+username+"' and password = '"+password+"' ")
        r = c.fetchone()
        
        if r:
            session["loggedin"] = True
            session["username"] = username
            return redirect(url_for("index"))
        else:
            msg = "Incorrect email/password"
    return render_template('login.html', msg = msg)


@app.route('/form')
def form():
    return render_template('predict.html')
  

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = None
    if(request.method == "POST"):
        if(request.form["username"]!= "" and request.form["password"]!= ""):
            username = request.form["username"]
            password = request.form["password"]
            conn = sqlite3.connect("register.db")
            c = conn.cursor()
            c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    ''')
            c.execute("INSERT INTO users VALUES('"+username+"',  '"+password+"')")
            msg = "Your account is created!!!"
            conn.commit()
            conn.close()
        else:
            msg = "Something wents wrong!!"      
    return render_template('register.html', msg = msg)


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact',methods=['POST','GET'])
def contact():
    msg = None
    if(request.method == "POST"):
        if(request.form["name"]!= "" and request.form["email"]!= "" and request.form["subject"]!= "" and request.form["message"]!= "" ):
            name = request.form['name']
            email = request.form['email']
            subject = request.form['subject']
            message = request.form['message']
            conn = sqlite3.connect("contacts.db")
            c = conn.cursor()
            c.execute('''
                      CREATE TABLE IF NOT EXISTS contacts (
                          name TEXT PRIMARY KEY,
                          email TEXT,
                          subject TEXT,
                          message TEXT
                          )
                          ''') 
            c.execute("INSERT INTO contacts VALUES('"+name+"',  '"+email+"', '"+subject+"', '"+message+"')")
            msg = "Message Sent!!!"
            conn.commit()
            conn.close()
        else:
            msg = "Something wents wrong!!" 
    return render_template('contact.html', msg = msg)


@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/feature')
def feature():
    return render_template('feature.html')


@app.route('/logout', methods =['GET', 'POST'])
def logout():
    if(request.method == "POST"):
        session.clear()
        return redirect(url_for('login'))
    return render_template('logout.html')

@app.route('/predict', methods=['POST'])
def predict():
	#Alternative Usage of Saved Model
    DT_Model = open(r'C:\Users\tanvi\PROJECT3\Decision_Tree_Model.pkl','rb')
    loaded_model = joblib.load(DT_Model)
    
    if request.method == 'POST': 
        gender = request.form['Gender']
        
        if gender == "Male":
            gender = 1.0
        else:
            gender = 0.0

        # Featch Value for Age
        age = float(request.form['Age'])

        # Fetch value for  Total Debt
        debt = float(request.form['Total_Debt'])

        # Fetch value for Total Professional Experience
        experience = float(request.form['Tot_Experience'])

        # Fetch value for Total Professional Experience
        income = float(request.form['Income'])

        # Fetch value for Bank Customer
        b_cust = request.form['Bank_Customer']
        if b_cust == "Genuine":
            b_cust = 0.0
        elif b_cust == "Government Guarantor":
            b_cust = 2.0
        else:
            b_cust = 1.0

        # Fetch value of Employment Status
        e_status = request.form['E_Status']
        if e_status == "t":
            e_status = 1.0
        else:
            e_status = 0.0

        # Fetch value for Credit Score
        cre_score = float(request.form['Credit_Score'])


        # Fetch value for Education Level
        e_level = request.form['Edu_Level']
        if e_level == "Workspace Training":
            e_level = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ,0.0, 0.0, 0.0]
        elif e_level == "Quality Control Expert":
            e_level = [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ,0.0, 0.0, 0.0]
        elif e_level == "Master's Degree":
            e_level = [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ,0.0, 0.0, 0.0]
        elif e_level == "Researcher":
            e_level = [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ,0.0, 0.0, 0.0]
        elif e_level == "Certified Course Professional":
            e_level = [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ,0.0, 0.0, 0.0]
        elif e_level == "Business Degree":
            e_level = [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0 ,0.0, 0.0, 0.0]
        elif e_level == "Completed High School":
            e_level = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0 ,0.0, 0.0, 0.0]
        elif e_level == "Diploma Holder":
            e_level = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0 ,0.0, 0.0, 0.0]
        elif e_level == "Diverse Background":
            e_level = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0 ,0.0, 0.0, 0.0]
        elif e_level == "IT Degree":
            e_level = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0 ,0.0, 0.0, 0.0]
        elif e_level == "Entrepreneurship Graduate":
            e_level = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0 ,0.0, 0.0, 0.0]
        elif e_level == "Agriculture Degree":
            e_level = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ,1.0, 0.0, 0.0]
        elif e_level == "Food Industry Degree":
            e_level = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ,0.0, 1.0, 0.0]
        else:
            e_level = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ,0.0, 0.0, 1.0]


        # Featch value for Prior Default
        default = request.form['Default']
        if default == "1":
            default = 0.0
        else:
            default = 1.0

        # Fetch value for Marital Status
        m_status = request.form['Mar_Status']
        if m_status == "Single":
            m_status = [1.0, 0.0, 0.0]
        elif m_status == "Married":
            m_status = [0.0, 1.0, 0.0]
        else:
            m_status = [0.0, 0.0, 1.0]

        # Fetch value for Citizenship
        citizen = request.form['Citizen']
        if citizen == "Yes":
            citizen = [1.0, 0.0, 0.0]
        elif citizen == "No":
            citizen = [0.0, 1.0, 0.0]
        else:
            citizen = [0.0, 0.0, 1.0]

        # Fetch value for Drivers Licence
        d_licence = request.form['D_Licence']
        if d_licence == "Yes":
            d_licence = [1.0, 0.0]
        else:
            d_licence = [0.0, 1.0]

        # Fetch value for Ethncity
        ethnicity = request.form['Ethnicity']
        if ethnicity == 'Asian':
            ethnicity = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        elif ethnicity == 'Hispanic':
            ethnicity = [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        elif ethnicity == 'Black':
            ethnicity = [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        elif ethnicity == 'White':
            ethnicity = [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        elif ethnicity == 'Jewish':
            ethnicity = [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0]
        elif ethnicity == 'Other':
            ethnicity = [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]
        elif ethnicity == 'Unknown':
            ethnicity = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0]
        elif ethnicity == 'Middle Eastern':
            ethnicity = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0]
        else:
            ethnicity = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]


        #newX1 = [gender, age, debt, b_cust, experience, default, e_status, cre_score, income] + m_status + e_level + citizen + d_licence + ethnicity
        newX1 = [0.0, 25, 0.07446429, 0.0, 0.00298246,0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0]
        newX2 = [1.0, 0.39849624, 0.76785714, 0.0, 0.70175439, 1.0, 1.0, 0.1641791, 0.024, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]

        if default == 0.0:
            newX = [newX2]
        else:
            newX = [newX1]

        X_nparray = np.asarray(newX, dtype=np.float32)

        my_prediction = loaded_model.predict(X_nparray)
    
    return render_template('result.html',prediction = my_prediction)


if __name__ == '__main__':
	app.run(debug=True)