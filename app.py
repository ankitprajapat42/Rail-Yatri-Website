from flask import Flask,render_template,request
import requests
import pymysql


# Database Connectivity 
db =pymysql.connect(
    host ='localhost', 
    user ='root',
    password='',
    port=3306,
    database='railyatari'
)


app=Flask(__name__)
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        cursor = db.cursor()
        cursor.execute(f"select email from accounts;")
        d = cursor.fetchall()
        emails_list = [i[0] for i in d]
        if email in emails_list:
            cursor.execute(f"select password from accounts where email='{email}'")
            data = cursor.fetchall()[0][0]
            if password == data:
                return render_template('index.html')
            else:
                return render_template('login.html', msg='Password Incorrect')
        else:
            return render_template('login.html', msg='Invalid User')

    else:
        return render_template('login.html')
    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
        Name = request.form.get('name')
        Email = request.form.get('email')
        Mobile_no = request.form.get('mobile_no')
        Password = request.form.get('password')
        cursor = db.cursor()
        cursor.execute(f"select email from accounts;")
        d = cursor.fetchall()
        emails_list = [i[0] for i in d]
        if Email in emails_list:
            return "This Email Already Used"
        else:
            cursor.execute(f"insert into accounts values('{Name}', '{Email}', {Mobile_no}, '{Password}');")
            cursor.fetchall()
            db.commit() 
            return render_template('signup.html', msg="Your Account is Created Go to Login")
            
    else:
        return render_template('Signup.html')
    

@app.route('/home')
def home():
    if request.method=='POST':
        data=request.form.get('pnr')
        print('Data ',data)
       
        url = f"https://irctc-indian-railway-pnr-status.p.rapidapi.com/getPNRStatus/{data}"

        headers = {
        "x-rapidapi-key": "8775ac996fmsh9b9e30fd95efd88p1032b6jsn5b39521a346d",
        "x-rapidapi-host": "irctc-indian-railway-pnr-status.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)
        result=response.json()
        if result['success']==True:
            d={
                'Date Of Journey':result['data']['dateOfJourney'],
                'Train Number' : result['data']['trainNumber'],
                'Train Name' : result['data']['trainName'],
                'Source Station': result['data']['sourceStation'],
                'Destination Station': result['data']['destinationStation'],
                'Boarding Point': result['data']['boardingPoint'],
                'No of Passengerss':result['data']['numberOfpassenger']
               }
            passenger=[]
            for i in result['data']['passengerList']:
                passenger.append([i['passengerSerialNumber'],i['bookingStatusDetails'],i['currentStatusDetails']])
            return render_template('index.html',d=d,passenger=passenger)
        else:
            return render_template('index.html',msg='No Such PNR Found')

        return 'Successfull'
    else:
        return render_template('index.html')

    


@app.route('/login')
def logout():
    return render_template('login.html')


if __name__=='__main__':
    app.run('localhost',1000,debug=True)


