from flask import Flask, render_template, url_for, request
import joblib
import sqlite3

model = joblib.load("./models/linear_model.lb")
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method == 'POST':  # int - because we need to pass int values to the model
        brand_name = int(request.form['brand_name'])
        Kms_Driven = int(request.form['Kms_Driven'])
        owner = int(request.form['owner'])
        age = int(request.form['age'])
        power = int(request.form['power'])

        # this is the dictionary in which we trained our model
        brand_dict = {'Bajaj': 1,'Royal Enfield': 2,'Hero': 3,'Honda': 4,
                       'Yamaha': 5,'TVS': 6,'KTM': 7,'Suzuki': 8,
                       'Harley-Davidson': 9,'Kawasaki': 10,'Hyosung': 11,
                       'Mahindra': 12,'Benelli': 13,'Triumph': 14,'Ducati': 15,
                       'BMW': 16}
        
        # we need to replace keys with their values if we want to store 
        # bike brand name in our database, otherwise instead of brand
        # name, integer value will be stored

        bike_brands = {value:key for key,value in brand_dict.items()}
        
        UNSEEN_DATA = [[Kms_Driven,owner,age,power,brand_name]]    # user input data
        # this order is important because in this order only, our algorithm is trained

        PREDICTION = model.predict(UNSEEN_DATA)[0][0]    # array([25421.25421])

        
        # inserting data into the database

        query_to_insert = """
        insert into bikedetails values(?,?,?,?,?,?)
        """

        conn = sqlite3.connect('bikedata.db')
        cur = conn.cursor()
        data = bike_brands[brand_name],Kms_Driven,owner,age,power,round(PREDICTION,2)
        # this order should be the same in which we created our table in database.py
        cur.execute(query_to_insert,data)
        conn.commit()  ###### ??????
        print('Your record has been stored in our database')
        cur.close()
        conn.close()

        return render_template('home.html',prediction_text=str(round(PREDICTION,2)))   
    

if __name__ == '__main__':
    app.run(debug=True)