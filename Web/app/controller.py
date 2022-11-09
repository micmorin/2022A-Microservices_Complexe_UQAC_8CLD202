import requests
import json
from flask import render_template, flash, redirect, url_for, request, make_response
from flask_login import login_user, logout_user, login_required, current_user
from models import LoginForm, RegisterForm, User
from config import DB
from datetime import datetime

########
# MAIN #
########

def main_index():
    if current_user.is_authenticated:
        pre = datetime.utcnow()
        response = requests.get(DB.MySQL_API_URL+'/objects/')
        requests.post(DB.MySQL_API_URL+'/metrics/create',data=json.dumps( {"access_page":"index","access_duration":round((datetime.utcnow()-pre).total_seconds()*1000)}), headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            return render_template('index.html', objects=response.json()['data'])
        else :
            flash(response.json()['message'])
            return render_template('index.html', objects="")
    return redirect(url_for('main.main_login')) 
    
def main_login():
    form = LoginForm()

# POST Request
    if form.is_submitted():
        pre = datetime.utcnow()
        response = requests.post(
            DB.MySQL_API_URL+'/login', 
            data=json.dumps( {
                "username":form.username.data,
                "password":form.password.data
            }), 
            headers={'Content-Type': 'application/json'})
        requests.post(DB.MySQL_API_URL+'/metrics/create',data=json.dumps( {"access_page":"login","access_duration":round((datetime.utcnow()-pre).total_seconds()*1000)}), headers={'Content-Type': 'application/json'})
    # Connection Reussie    
        if response.status_code == 200:
            requests.get(DB.IoT_API_URL+'/init_db')

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
            next = request.args.get('next')
            return redirect(next or url_for('main.main_index'))
        
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
    form=RegisterForm()
    if current_user.profil == 'admin':
        pre = datetime.utcnow()
        response = requests.get(DB.MySQL_API_URL+'/users/')
        requests.post(DB.MySQL_API_URL+'/metrics/create',data=json.dumps( {"access_page":"users","access_duration":round((datetime.utcnow()-pre).total_seconds()*1000)}), headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            return render_template('user_list.html', users=response.json()['data'], form=form)
        else :
            flash(response.json()['message'])
            return render_template('user_list.html', users="", form=form)
    return redirect(url_for('main.main_index'))

@login_required
def user_create():
    form=RegisterForm()

# POST Request
    if form.is_submitted():
        pre = datetime.utcnow()
        response = requests.post(
            DB.MySQL_API_URL+'/users/create', 
            data=json.dumps( {
                "name":form.name.data,
                "username":form.username.data,
                "email":form.email.data,
                "password":form.password.data
            }), 
            headers={'Content-Type': 'application/json'})
        requests.post(DB.MySQL_API_URL+'/metrics/create',data=json.dumps( {"access_page":"create_user","access_duration":round((datetime.utcnow()-pre).total_seconds()*1000)}), headers={'Content-Type': 'application/json'})
    
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
        pre = datetime.utcnow()
        response = requests.put( DB.MySQL_API_URL+'/users/update', 
            data=json.dumps( {
                "id":user_id,
                "name":request.form['name'],
                "username":request.form['username'],
                "email":request.form['email'],
                "password":password
                #"profilID":request.form['profil']
            }), 
            headers={'Content-Type': 'application/json'})
        requests.post(DB.MySQL_API_URL+'/metrics/create',data=json.dumps( {"access_page":"update_user","access_duration":round((datetime.utcnow()-pre).total_seconds()*1000)}), headers={'Content-Type': 'application/json'})

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
        pre = datetime.utcnow()
        response = requests.delete( DB.MySQL_API_URL+'/users/delete', 
            data=json.dumps( {
                "id":user_id
            }), 
            headers={'Content-Type': 'application/json'})
        requests.post(DB.MySQL_API_URL+'/metrics/create',data=json.dumps( {"access_page":"delete_user","access_duration":round((datetime.utcnow()-pre).total_seconds()*1000)}), headers={'Content-Type': 'application/json'})

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
        pre = datetime.utcnow()
        response = requests.get(DB.MySQL_API_URL+'/profils')
        requests.post(DB.MySQL_API_URL+'/metrics/create',data=json.dumps( {"access_page":"profils","access_duration":round((datetime.utcnow()-pre).total_seconds()*1000)}), headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            return render_template('profil_list.html', profils=response.json()['data'])
        else :
            flash(response.json()['message'])
    return redirect(url_for('main.main_index'))

@login_required
def profil_create():
    if current_user.profil == "admin":
        pre = datetime.utcnow()
        response = requests.post( DB.MySQL_API_URL+'/profils/create', 
            data=json.dumps( {
                "description":request.form['description']
            }), 
            headers={'Content-Type': 'application/json'})
        requests.post(DB.MySQL_API_URL+'/metrics/create',data=json.dumps( {"access_page":"profil_create","access_duration":round((datetime.utcnow()-pre).total_seconds()*1000)}), headers={'Content-Type': 'application/json'})

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
        pre = datetime.utcnow()
        response = requests.put( DB.MySQL_API_URL+'/profils/update', 
            data=json.dumps( {
                "id":profil_id,
                "description":request.form['description']
            }), 
            headers={'Content-Type': 'application/json'})
        requests.post(DB.MySQL_API_URL+'/metrics/create',data=json.dumps( {"access_page":"profil_update","access_duration":round((datetime.utcnow()-pre).total_seconds()*1000)}), headers={'Content-Type': 'application/json'})

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
        pre = datetime.utcnow()
        response = requests.delete( DB.MySQL_API_URL+'/profils/delete', 
            data=json.dumps( {
                "id":profil_id
            }), 
            headers={'Content-Type': 'application/json'})
        requests.post(DB.MySQL_API_URL+'/metrics/create',data=json.dumps( {"access_page":"profil_delete","access_duration":round((datetime.utcnow()-pre).total_seconds()*1000)}), headers={'Content-Type': 'application/json'})

    # Delete Reussie    
        if response.status_code == 200:
            flash('Suppression reussie')
            
    # Delete Echoue
        else:
            flash(response.json()['message'])
        return redirect(url_for('profil.profil_index'))    

    return redirect(url_for('main.main_index'))

##########
# OBJECT #
##########
@login_required
def object_create():
    pre = datetime.utcnow()
    response = requests.post( DB.IoT_API_URL+'/', 
        data=json.dumps( {"type":request.form['type']} ), 
        headers={'Content-Type': 'application/json'})
    requests.post(DB.MySQL_API_URL+'/metrics/create',data=json.dumps( {"access_page":"object_create","access_duration":round((datetime.utcnow()-pre).total_seconds()*1000)}), headers={'Content-Type': 'application/json'})

    # Update Reussie    
    if response.status_code == 200:
        flash(response.json()['data'])
    
    # Update Echoue
    else:
        flash(response.json()['message'])
    
    return redirect(url_for('simulator.simulator_index'))

@login_required
def object_update(object_id):
    pre = datetime.utcnow()
    response = requests.put( DB.MySQL_API_URL+'/objects/update', 
        data=json.dumps( {
            "id":object_id,
            "nom":request.form['nom'],
            "status":request.form['status_radio_'+str(object_id)]
        }), 
        headers={'Content-Type': 'application/json'})
    requests.post(DB.MySQL_API_URL+'/metrics/create',data=json.dumps( {"access_page":"object_update","access_duration":round((datetime.utcnow()-pre).total_seconds()*1000)}), headers={'Content-Type': 'application/json'})

    # Update Reussie    
    if response.status_code == 200:
        if request.form['status_radio_'+str(object_id)] == 1:
            requests.post( DB.IoT_API_URL+'/confirm', 
            data=json.dumps( {"nom":request.form['nom'], "type_obj":request.form['type_obj']}), 
            headers={'Content-Type': 'application/json'})     
        flash('Modification reussie')
    
    # Update Echoue
    else:
        flash(response.json()['message'])
    
    return redirect(url_for('main.main_index'))
    

#############
# SIMULATOR #
#############
@login_required
def simulator_index():
    pre = datetime.utcnow()
    response = requests.get(DB.MySQL_API_URL+'/objects/')
    requests.post(DB.MySQL_API_URL+'/metrics/create',data=json.dumps( {"access_page":"simulator","access_duration":round((datetime.utcnow()-pre).total_seconds()*1000)}), headers={'Content-Type': 'application/json'})

    if response.status_code == 200:
        return render_template('simulation.html', objects=response.json()['data'])
    else :
        flash(response.json()['message'])
        return render_template('simulation.html', objects="")

@login_required
def simulator_create():
    IO = True
    if request.form['IO_'+request.form['id']] == 1:
        IO = False
    mesures =[IO]
    mesures.append(request.form['measure1_'+request.form['id']])
    if request.form['type_obj'] == 'Sonde_Niveau_Eau':
        mesures.append(request.form['measure2_'+request.form['id']])
    
    pre = datetime.utcnow()
    response = requests.post( DB.IoT_API_URL+'/data/create', 
        data=json.dumps( 
            {
                "nom": request.form['nom'],
                "type" : request.form['type_obj'],
                "measures" : mesures,
                "token": request.form['token'],
                "status": request.form['status']
            } ), 
        headers={'Content-Type': 'application/json'})
    requests.post(DB.MySQL_API_URL+'/metrics/create',data=json.dumps( {"access_page":"simulator_create","access_duration":round((datetime.utcnow()-pre).total_seconds()*1000)}), headers={'Content-Type': 'application/json'})

    flash(response.json()['message'])
    
    return redirect(url_for('simulator.simulator_index'))

#############
# ANALYTICS #
#############
@login_required
def analytics_index():
    pre = datetime.utcnow()
    response = requests.get(DB.IoT_API_URL+'/analytics')
    requests.post(DB.MySQL_API_URL+'/metrics/create',data=json.dumps( {"access_page":"analytics","access_duration":round((datetime.utcnow()-pre).total_seconds()*1000)}), headers={'Content-Type': 'application/json'})

    return render_template(
        'analytics.html',
        iotdb_records=response.json()['iotdb_records'],
        iotdb_metrics=response.json()['iotdb_metrics'],
        mysql_records=response.json()['mysql_records'],
        mysql_metrics=response.json()['mysql_metrics'],
        summary=response.json()['summary'],
        )

@login_required
def analytics_delete():
    pre = datetime.utcnow()
    response = requests.delete( DB.IoT_API_URL+'/data/delete', 
    data=json.dumps( 
        {
            "nom": request.form['nom'],
            "time" : request.form['time'],
            "type" : request.form['type']
        } ), 
        headers={'Content-Type': 'application/json'})
    requests.post(DB.MySQL_API_URL+'/metrics/create',data=json.dumps( {"access_page":"analytics_delete","access_duration":round((datetime.utcnow()-pre).total_seconds()*1000)}), headers={'Content-Type': 'application/json'})

    flash(response.json()['message'])
    
    return redirect(url_for('analytics.analytics_index'))
