from flask import Flask, render_template, url_for,request,flash, redirect, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from funciones import *
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
@login_required
def index():
    return render_template("index.html",username=session["username"])

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not request.form.get("username"):
            flash('Ingrese un nombre de usuario')
            return redirect("/login")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash('Ingrese una contraseña')
            return redirect("/login")
        
        user = db.execute("SELECT * FROM users WHERE username = '"+str(username)+"'").fetchall()
        
        # Ensure username exists and password is correct
        if len(user) != 1 or not check_password_hash(user[0]["password"], password):
            flash('Contraseña Incorrecta')
            return redirect("/login")

        # Remember which user has logged in
        session["id_user"] = user[0]["id_user"]
        session["username"] = username

        return redirect('/')
    else:    
        return render_template("login.html")



@app.route("/register", methods=["POST","GET"])
def register():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Ingrese un nombre de usuario")
            return redirect("/register")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Ingrese una contraseña")
            return redirect("/register")

        elif not request.form.get("email"):
            flash("Ingrese un correo")
            return redirect("/register")
        
        elif not request.form.get("cedula"):
            flash("Ingrese una cedula")

        elif not request.form.get("name"):
            flash("Ingrese su nombre")
            return redirect("/register")
        
        elif not request.form.get("lastname"):
            flash("Ingrese su apellido")
            return redirect("/register")
        
        elif not request.form.get("birthday"):
            flash("Ingrese su fecha de cumpleaños")
            return redirect("/register")
        
        elif not request.form.get("phone"):
            flash("Ingrese su numero de celular")
            return redirect("/register")

        elif not request.form.get("city"):
            flash("Ingrese un departamento")
            return redirect("/register")
    
        elif not request.form.get("postalcode"):
            flash("Ingrese su codigopostal")
            return redirect("/register")

        
        #datos persona
        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))
        email = request.form.get("email")
        cedula = request.form.get("cedula")
        name = request.form.get("name")
        lastname = request.form.get("lastname")
        birthday = request.form.get("birthday")
        phone = request.form.get("phone")
        city = request.form.get("city")
        postalcode = request.form.get("postalcode")
        sex = request.form.get("select")

        # Query database for person
        db.execute("INSERT INTO person (cedula,name,lastname,birthday,phone,country,city,postalcode,sex) VALUES ('"+str(cedula)+"','"+str(name)+"','"+str(lastname)+"','"+str(birthday)+"','"+str(phone)+"','Nicaragua','"+str(city)+"','"+str(postalcode)+"','"+str(sex)+"')")
        db.commit()
        # Query selection id person
        user = db.execute("SELECT * FROM person WHERE cedula = '"+cedula+"'").fetchall()
        # Query database for users
        db.execute("INSERT INTO users (username,password,email,id_person) VALUES ('"+str(username)+"','"+str(password)+"','"+str(email)+"',"+str(user[0]["id_person"])+")")
        db.commit()
        # Redirect user to home page
        return redirect("/login")
    else:
        return render_template('register.html')

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect('/')

@app.route("/admin", methods=["GET","POST"])
@login_required
def admin():
    return render_template('admin.html')

@app.route("/products", methods=["GET","POST"])
@login_required
def products():
    return render_template('products.html')
