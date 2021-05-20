from flask import Flask,render_template,request,redirect
from flask_login import login_required, current_user, login_user, logout_user
from models import UserModel,db,login


app = Flask(__name__, template_folder='templates') 
app.secret_key = 'c23e98ecmkosmcodm1'
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userdata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login.init_app(app)
login.login_view = 'login'


@app.before_first_request
def create_all():
    db.create_all()



# search page
@app.route('/main')
@login_required
def mainPage():
    return render_template('main.html')

# invalid username/email
@app.route('/invalidemail')
def invalidEmail():
    return render_template('invalidemail.html')
@app.route('/invalidusername')
def invalidUsername():
    return render_template('invalidusername.html')



# login page
@app.route('/', methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/main')
     
    if request.method == 'POST':
        email = request.form['email']
        user = UserModel.query.filter_by(email = email).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect('/main')
        else:
            return render_template("invalidlogin.html")

    return render_template('index.html')
 
@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect('/main')
     
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
 
        if UserModel.query.filter_by(email=email).first():
           return redirect("invalidemail")
        if UserModel.query.filter_by(username=username).first():
           return redirect("invalidusername")

        user = UserModel(email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    return render_template('register.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

if __name__ == '__main__':
    app.run()
