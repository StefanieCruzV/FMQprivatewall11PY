from crypt import methods
from flask_app import app
from flask import render_template,redirect,request,session
from flask_app.models import from_to
from flask_app.models import login
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import flash

@app.route("/")
def index():
    return render_template("index.html") 

@app.route("/success")
def success():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    all_user_info = login.Login.get_all_user_info(data)
    all_user_messages_list = from_to.From_to.get_all_user_messages(data)
    all_user_db = login.Login.get_all_user_db(data)
    return render_template("response.html", user=all_user_info, messages=all_user_messages_list, all_user_db=all_user_db)

@app.route("/newuser", methods=["POST"])
def newuser():
    
    pw_hash = bcrypt.generate_password_hash(request.form['password']) # crear Hash del password
    print(pw_hash)
    data = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
            "password": pw_hash
        }
    user_id = login.Login.save(data)
    session['user_id'] = user_id
    return redirect('/success')

@app.route("/login", methods=["POST"])
def login_fun():
    if not login.Login.validate_login(request.form): # is la validacion es falso mandamos a index
        return redirect('/')
    # see if the username provided exists in the database
    data = { 
        "email" : request.form["email"] 
        }
    user_in_db = login.Login.get_by_email(data)
    # user is not registered in the db
    if not user_in_db: # Si es falso, que no hay un email in la Base de Datos
        flash("Invalid Email/Password")
        return redirect("/")
    # Si es verdadero, crear el HASH del password de la forma, y verificar so el HASH de la Base de Datos es el mismo
    # Recibe dos parametros, el primero es el HASH de la Base de Datos y el segundo el password de la forma del HTML, y los compara
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect('/success')
 

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/delete_message/<int:message_id>/<int:from_id>")
def delete_message(message_id, from_id):
    data = {
        'from_id': from_id,
        'message_id': message_id
    }
    print(data)
    from_to.From_to.delete_message(data)
    return redirect('/success')

@app.route("/create_message", methods=["POST"])
def create_message():
    print(request.form)
    message_data = {
        'message': request.form['message']
    }
    message_id = login.Login.create_message(message_data)

    from_to_data = {
        'form_id': session['user_id'],
        'to_id': request.form['to_id'],
        'message_id': message_id
    }
    from_to.From_to.create_relation_message(from_to_data)
    return redirect('/success')
