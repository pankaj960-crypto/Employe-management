from symtable import Class


from flask import Flask, render_template,url_for,redirect,flash,request,session
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'Secret Key'
#databaset set up
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/crud'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(100) ,nullable=False)
    email = db.Column(db.String(100),nullable=False)
    phone = db.Column(db.String(100))
    department = db.Column(db.String(100))
    def __init__(self, name, email, phone, department):
        self.name = name
        self.email = email
        self.phone = phone
        self.department = department

#inserting data
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        department = request.form['department']
        data = Data(name, email, phone, department)
        db.session.add(data)
        db.session.commit()
        flash('Employee inserted successfully')
        return redirect(url_for('service'))


# #udate
@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        data = Data.query.get(request.form.get('id'))
        data.name = request.form['name']
        data.email = request.form['email']
        data.phone = request.form['phone']
        data.department = request.form['department']
        db.session.commit()
        flash('Employee updated successfully')
        return redirect(url_for('service'))
#delet
@app.route('/delete/<id>/', methods=['GET','POST'])
def delete(id):
    data = Data.query.get(id)
    db.session.delete(data)
    db.session.commit()
    flash('Employee deleted successfully')
    return redirect(url_for('service'))






@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html',current_year=datetime.now().year)
@app.route('/about')
def about():
    return render_template('about.html',current_year=datetime.now().year)

#welcome
@app.route('/welcome')
def welcome():
     return render_template('welcome.html')




#register


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    confirm_password = db.Column(db.String(200), nullable=False)

    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def __init__(self, name, email, password, confirm_password):
        self.name = name
        self.email = email
        self.password = password
        self.confirm_password = confirm_password

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if email already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists!", "danger")
            return redirect(url_for('register'))

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('register'))

        # ✅ Create new user and hash password
        new_user = User(name, email, password, confirm_password)
        new_user.set_password(password)  # This line creates password_hash

        # (Optional) If your User table still has password/confirm_password columns
        new_user.password = password
        new_user.confirm_password = confirm_password

        # Save to database
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html', current_year=datetime.now().year)

    #     if password != confirm_password:
    #         flash("Passwords do not match!", "danger")
    #         return redirect(url_for('register'))
    #
    #     existing_user = User.query.filter_by(email=email).first()
    #     if existing_user:
    #         flash("Email already registered!", "warning")
    #         return redirect(url_for('register'))
    #
    #     new_user = User(name, email, password, confirm_password)
    #     db.session.add(new_user)
    #     db.session.commit()
    #
    #     # In a real app, you'd save the user to the database here
    #     flash("Account created successfully! Please log in.", "success")
    #     return redirect(url_for('login'))
    #         #redirect(url_for('login')))
    #
    # return render_template('register.html', current_year=datetime.now().year)






#login code
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        # Simple demo authentication (replace with database check later)
        # if username == username and password == password:
        #     session['user'] = username
        #     flash("Login successful!", "success")
        #     return render_template('welcome.html',name=username)
        # else:
        #     flash("Invalid email or password. Try again.", "danger")
        #     return redirect(url_for('login'))

        if user and user.check_password(password):
            session['user'] = user.name
            flash("Login successful!", "success")
            return render_template('welcome.html', name=user.name)
        else:
            flash("Invalid email or password. Try again.", "danger")
            return redirect(url_for('login'))

    return render_template('login.html', current_year=datetime.now().year)



# @app.route('/welcome')
# def welcome():
#     if 'user' in session:
#         return render_template('welcome.html', name=session['user'])
#
#     return redirect(url_for('login'))
# Welcome page after login






@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))


#service Employee
@app.route('/service')
def service():
    all_data = Data.query.all()

    return render_template('service.html', employees = all_data)


if __name__ == '__main__':
    app.run(debug=True)