from flask import Blueprint , render_template ,request ,flash ,redirect ,url_for
from .model import User ,Note
from werkzeug.security import generate_password_hash , check_password_hash
from .import db
from flask_login import login_user,login_required,logout_user,current_user


auth = Blueprint('auth',__name__)


@auth.route("/login",methods=['GET','POST'])
def login():

    if request.method =="POST":

        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password,password) :
                login_user(user,remember=True)
                flash("Logged in Successfully",category="success")
                return redirect(url_for("views.home"))
            else:
                flash("Invalid email or password",category="error")
        else:
            flash("Email does not exists. Please create an account",category="error")
            return redirect(url_for("auth.signup"))


    return render_template("login.html",user=current_user)


@auth.route("/logout",methods=['GET','POST'])
@login_required
def logout ():
    logout_user()
    flash("Logout successfully", category="info")
    return redirect(url_for("auth.login"))



@auth.route("/sign-up",methods=['GET','POST'])
def signup():
    if request.method =="POST":

        # Getting values
        email = request.form['email']
        firstname = request.form['firstname']
        password1 = request.form['password']
        password2 = request.form['password2']

        print(email,firstname,password1,password2)

        # applying checks
        user = User.query.filter_by(email=email).first()

        if user:
            flash("User exists" ,category="error") 
            return redirect(url_for("auth.login"))
        elif len(email) <4:
            flash('Email must be greater then 4 character',category="error")

        elif len(firstname)<2:
            flash('First name should be greater then 1 character',category="error")

        elif password2 != password1:
            flash('Both passwords should match',category="error")

        elif len(password1)<6:
            flash('Passwords should be greater then 7 character',category="error")

        else:
            # add the user to the database
            new_user = User(email=email , password= generate_password_hash(password1,method="sha256"),first_name=firstname)
            db.session.add(new_user)
            db.session.commit()
            login_user(user)
            flash(f'Account created with name "{new_user.first_name}"',category="success")
            return redirect(url_for('views.home'))
    return render_template("signup.html",user=current_user)

