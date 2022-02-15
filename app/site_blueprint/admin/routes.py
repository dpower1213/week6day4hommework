from .import bp as admin
from .forms import LoginForm, RegistrationForm, EditProfileForm
from flask import render_template, request, flash, redirect, url_for
from app.models import User, db
# User_Join_Pokemon
from flask_login import login_user, current_user, logout_user, login_required

@admin.route('/registration', methods=['GET','POST'])
def registration():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user_data = {
            "name_first":form.name_first.data.title(),
            "name_last":form.name_last.data.title(),
            "email":form.email.data.lower(),
            "password":form.password.data 
            }
            new_user_object=User()
            new_user_object.from_dict(new_user_data)
            new_user_object.save()
                
        except:
            flash('Oooppps, that was awful......awful entertaining')
            return render_template('registration.html.j2',form=form)
    
        flash('You have sucessfully given your information to us for sale to data aggregation companies')
        return redirect(url_for('admin.login'))
    return render_template('registration.html.j2',form = form)

@admin.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method== 'POST' and form.validate_on_submit():
        email = request.form.get('email').lower()
        password = request.form.get('password')
        u = User.query.filter_by(email=email).first()
        if u and u.check_hashed_password(password):
            login_user(u)
            flash('Welcome:)','success')
            return redirect(url_for('site.index'))
        flash('Oooppps, that was awful......awful entertaining')
        return render_template('login.html.j2', form=form)
    return render_template('login.html.j2', form=form)
    
@admin.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        flash('You have logged out', 'warning')
        return redirect(url_for('admin.login'))

@admin.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_user_data={
                "name_first":form.name_first.data.title(),
                "name_last":form.name_last.data.title(),
                "email":form.email.data.lower(),
                "password":form.password.data
        }
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.email != current_user.email:
            flash('Email already in use','danger')
            return redirect(url_for('admin.edit_profile'))
        try:
            current_user.from_dict(new_user_data)
            current_user.save()
            flash('Profile Updated', 'success')
        except:
            flash('There was an unexpected Error. Please Try again', 'danger')
            return redirect(url_for('admin.edit_profile'))
        return redirect(url_for('site.index'))
    return render_template('registration.html.j2', form = form)
    
@admin.route('/attack')
@login_required
def attack():
    users=User.query.filter(User.user_id != current_user.user_id).all()
    return render_template('/attack.html.j2', users = users)
    
@admin.route('/fight/<int:id>')
@login_required
def fight(id):
    user2=id
    user2=User.query.get(id)
    cluser_1=current_user.pokemen.all()
    cluser_2=user2.pokemen.all()
    points1=0
    points2=0
    
    for pokemon in cluser_1:
        points1 += pokemon.stat_rating1
    flash(f"{points1}")
        
    for pokemon in cluser_2:
        points2 += pokemon.stat_rating1
    flash(f"{points2}")
        
    if points1 > points2:
        current_user.wins += 1
        user2.losses += 1
        db.session.commit()
        flash('Fighter 1 wins!!!')
    else:
        current_user.losses +=1
        user2.wins +=1
        db.session.commit()
        flash('Fighter 2 wins!!!')
    return redirect(url_for('admin.attack'))