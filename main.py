from flask import Flask , redirect , url_for , request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import (LoginManager,UserMixin,current_user,login_required,login_user,logout_user)

from flask_principal import Principal,Permission,RoleNeed





app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///booking.db'
app.config['SECRET_KEY'] = 'secret_key'
db = SQLAlchemy(app)

loginManager = LoginManager(app)
principal = Principal(app) 

class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key= True)
    username = db.Column(db.String(50),unique= True,nullable=False)
    password = db.Column(db.String(50),nullable= False)

@loginManager.user_loader

def loaduser(user_id):
    return User.query.get(int(user_id))


@app.route('/login',methods=['GET','POST'])

def login():
    if request.method  == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username = username,password = password).first()
        if user:
            login_user(user)
            return redirect(url_for('home'))
        else:
            return "Invalid Username or Password!"
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method  == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        existuser = User.query.filter_by(username = username,password = password).first()
        if existuser:
            return "Username already exists"
        new_user = User(username = username,password = password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')




class Booking(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String[100], nullable = False)
    email = db.Column(db.String[100], nullable = False)
    mobile = db.Column(db.String[100], nullable = True)

@app.route('/')

def home():
    return render_template('index.html',name='Abdullah')

@app.route('/booking')

def booking():
    
    return render_template('booking.html')

@app.route('/allbooking')

def allbooking():
    all_bookimgs = Booking.query.all()
    return render_template('bookings.html',bookings=all_bookimgs)

@app.route('/book/',methods=['post'])

def book():
    name = request.form.get('name')
    email = request.form.get('email')
    mobile = request.form.get('mobile')
    booking = Booking(name=name,email=email,mobile=mobile)
    db.session.add(booking)
    db.session.commit()
    return redirect(url_for('allbooking'))

if __name__== '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)