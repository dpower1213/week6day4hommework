from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class PokemonForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    submit = SubmitField('Pokemon Name')
    
    # poke_id = StringField(validators=[DataRequired()])
    # submit2 = SubmitField('Pokemen Delete')
    
