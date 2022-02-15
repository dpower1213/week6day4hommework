from sqlalchemy import false
from .import bp as site
from flask import render_template, request, flash, redirect, url_for
import requests
from flask_login import login_required, current_user
from .forms import PokemonForm
from app.models import Pokemon, User, db, UserJoinPokemon

@site.route('/', methods = ['GET', 'POST'])
@login_required
def pokemon():
    form = PokemonForm()
    if request.method == 'POST' and form.validate_on_submit():
        #contact the api and get the info for the pokemon from the form
        
        if len(current_user.pokemen.all()) > 5:
            flash('You have too many pokemon, dont be greedy')
        else:
            name = request.form.get('name')
            print('hello', name)
            url = f"https://pokeapi.co/api/v2/pokemon/{name}"
            response = requests.get(url)
            if response.ok:
                data = response.json()            
                poke_dict = {
                    'name':data['forms'][0]['name'],
                    'order':data['order'],
                    'ability':data['abilities'][0]['ability']['name'],
                    'base_experience':data['base_experience'],
                    'front_shiny':data['sprites']['front_shiny'],
                    'stat_name1':data['stats'][0]['stat']['name'],
                    'stat_rating1':data['stats'][0]['base_stat'],
                    'stat_name2':data['stats'][1]['stat']['name'],
                    'stat_rating2':data['stats'][1]['base_stat'],
                    'stat_name3':data['stats'][2]['stat']['name'],
                    'stat_rating3':data['stats'][2]['base_stat']
                }
                
                if not Pokemon.exists(poke_dict['name']):
                    new_poke = Pokemon()
                    new_poke.poke_dictionary(poke_dict)
                    current_user.pokemen.append(new_poke)
                    new_poke.save()
                    flash('Pokemon sucessfully added to your team')
                    return render_template('pokemon.html.j2', poke = poke_dict, form=form)
                    
                else:
                    if not current_user.exists(poke_dict['name']):
                        new_poke=Pokemon.query.filter_by(name=name).first()
                        current_user.pokemen.append(new_poke)
                        current_user.save()
                        flash('Pokemon sucessfully added to your team2')
                        return render_template('pokemon.html.j2', poke = poke_dict, form=form)
                    else:
                        flash('You Already Have this Pokemon!')
                        return render_template('pokemon.html.j2', poke = poke_dict, form=form)
            else:
                flash('Yo, dingleberry, enter a valid name!')
    return render_template('pokemon.html.j2',form=form)

@site.route('/delete_poke/<int:id>')
@login_required
def delete_poke(id):
    poke_to_delete = Pokemon.query.get(id)
    try:
        current_user.pokemen.remove(poke_to_delete)
        db.session.commit()
        flash('Pokemon Sucessfully Deleted')
        return redirect(url_for('site.pokemon'))
    except:
        "Error Deleting the Pokemon"
    return redirect(url_for('site.pokemon'))
        
@site.route('/')
def index():
    return render_template('index.html.j2')