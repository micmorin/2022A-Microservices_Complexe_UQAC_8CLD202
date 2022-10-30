import requests
import json
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from models import LoginForm, RegisterForm, User
from config import DB

########
# MAIN #
########

def main_index():
    return render_template('index.html')

def main_login():
    form = LoginForm()

# POST Request
    if form.is_submitted():
        response = requests.post(
            DB.URL+'/login', 
            data=json.dumps( {
                "username":form.username.data,
                "password":form.password.data
            }), 
            headers={'Content-Type': 'application/json'})

    # Connection Reussie    
        if response.status_code == 200:

            # Set up User
            data = response.json()["data"]
            user = User(id = data['id'],
                name = data['name'],
                username = data['username'],
                email = data['email'],
                profil = data['profil'],
                token = data['token'])

            # Login User
            login_user(user)
            User.c_user = user

            # Redirect
            flash('Connexion reussie')
            return redirect(url_for('main.main_index')) 
        
    # Connection Echoue
        else:
            flash('Identifiants invalides.')
            return redirect(url_for('main.main_login')) 
    
# GET Request
    else:
        return render_template("login.html", form = form)

@login_required
def main_logout():
    logout_user()
    return redirect('/')

########
# USER #
########

@login_required
def user_index():
    if current_user.profil == 'admin':
        response = requests.get(DB.URL+'/users/')
        if response.status_code == 200:
            return render_template('user_list.html', users=response.json()['data'])
        else :
            flash(response.json()['message'])
            return render_template('user_list.html', users="")
    return redirect(url_for('main.main_index'))

def user_create():
    form=RegisterForm()

# POST Request
    if form.is_submitted():
        response = requests.post(
            DB.URL+'/users/create', 
            data=json.dumps( {
                "name":form.name.data,
                "username":form.username.data,
                "email":form.email.data,
                "password":form.password.data
            }), 
            headers={'Content-Type': 'application/json'})

    # Ajout Reussie    
        if response.status_code == 200:
            if not current_user.is_authenticated:
                # Login User
                data = response.json()
                user = User(
                    name=form.name.data, 
                    username=form.username.data, 
                    email=form.email.data,
                    id=data['id'],
                    token=data['token'],
                    profil="user"
                    )
                login_user(user)
                User.c_user = user

            # Redirect
            if current_user.profil == "admin":
                flash('Ajout reussie')
                return redirect(url_for('user.user_index'))
            else:
                flash('Connexion reussie')
                return redirect(url_for('main.main_index')) 
        
    # Ajout Echoue
        else:
            flash(response.json()['message'])
            return redirect(url_for('user.user_create')) 

# GET Request
    else:
        return render_template('user_create.html', form=form)

@login_required
def user_update(user_id):
    if user_id == current_user.id or current_user.profil == "admin":
        password = "?"
        if request.form['password'] != "":
                        password = request.form['password']
        response = requests.put( DB.URL+'/users/update', 
            data=json.dumps( {
                "id":user_id,
                "name":request.form['name'],
                "username":request.form['username'],
                "email":request.form['email'],
                "password":password
                #"profilID":request.form['profil']
            }), 
            headers={'Content-Type': 'application/json'})


        # Update Reussie    
        if response.status_code == 200:
            if user_id == current_user.id:
                # Update User
                user = User(
                    name=request.form['name'], 
                    username=request.form['username'], 
                    email=request.form['email'],
                    id=current_user.id,
                    token=current_user.token,
                    #profil=request.form['profil']
                    )
                logout_user()
                login_user(user)
                User.c_user = user

            # Redirect
            flash('Changement reussie')
            if current_user.profil == "admin":
                return redirect(url_for('user.user_index'))
            else:
                return redirect(url_for('main.main_index')) 
        
    # Update Echoue
        else:
            flash(response.json()['message'])
    return redirect(url_for('main.main_index'))

@login_required
def user_destroy(user_id):
    if current_user.profil == "admin":
        response = requests.delete( DB.URL+'/users/delete', 
            data=json.dumps( {
                "id":user_id
            }), 
            headers={'Content-Type': 'application/json'})


    # Delete Reussie    
        if response.status_code == 200:
            flash('Suppression reussie')
            return redirect(url_for('user.user_index'))
        
    # Delete Echoue
        else:
            flash(response.json()['message'])
    return redirect(url_for('main.main_index'))

##########
# PROFIL #
##########
@login_required
def profil_index():
    if current_user.profil == 'admin':
        response = requests.get(DB.URL+'/profils')
        if response.status_code == 200:
            return render_template('profil_list.html', profils=response.json()['data'])
        else :
            flash(response.json()['message'])
    return redirect(url_for('main.main_index'))

@login_required
def profil_create():
    if current_user.profil == "admin":
        response = requests.post( DB.URL+'/profils/create', 
            data=json.dumps( {
                "description":request.form['description']
            }), 
            headers={'Content-Type': 'application/json'})

        # Create Reussie    
        if response.status_code == 200:
            flash('Creation reussie')
            return redirect(url_for('profil.profil_index'))
        
        # Create Echoue
        else:
            flash(response.json()['message'])
            return redirect(url_for('profil.profil_index'))

    return redirect(url_for('main.main_index'))

@login_required
def profil_update(profil_id):
    if  current_user.profil == "admin":
        response = requests.put( DB.URL+'/profils/update', 
            data=json.dumps( {
                "id":profil_id,
                "description":request.form['description']
            }), 
            headers={'Content-Type': 'application/json'})


        # Update Reussie    
        if response.status_code == 200:
           if response.status_code == 200:
            flash('Modification reussie')
            return redirect(url_for('profil.profil_index'))
        
        # Update Echoue
        else:
            flash(response.json()['message'])
            return redirect(url_for('profil.profil_index'))

    return redirect(url_for('main.main_index'))

@login_required
def profil_destroy(profil_id):
    if current_user.profil == "admin":
        response = requests.delete( DB.URL+'/profils/delete', 
            data=json.dumps( {
                "id":profil_id
            }), 
            headers={'Content-Type': 'application/json'})


    # Delete Reussie    
        if response.status_code == 200:
            flash('Suppression reussie')
            
    # Delete Echoue
        else:
            flash(response.json()['message'])
        return redirect(url_for('profil.profil_index'))    

    return redirect(url_for('main.main_index'))

##########
# CALCUL #
##########
@login_required
def calcul_index():
    response = requests.post( DB.URL+'/calculs/', 
            data=json.dumps( {
                "user_id":current_user.id
            }), 
            headers={'Content-Type': 'application/json'})

    if response.status_code == 200:
        return render_template('calcul_list.html', calculs=response.json()['data'])
    else :
        flash(response.json()['message'])
        return redirect(url_for('main.main_index'))

@login_required
def calcul_destroy(calcul_id):
    response = requests.delete( DB.URL+'/calculs/delete', 
        data=json.dumps( {
            "user_id":current_user.id,
            "id":calcul_id
        }), 
        headers={'Content-Type': 'application/json'})


# Delete Reussie    
    if response.status_code == 200:
        flash('Suppression reussie')
        
# Delete Echoue
    else:
        flash(response.json()['message'])
    return redirect(url_for('calcul.calcul_index'))    