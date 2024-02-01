from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy
import csv

#https://www.google.com/maps/place/Manchester

# Flask  Application Setup
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///caffees.db"
db = SQLAlchemy()
db.init_app(app)


class Caffees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cafe = db.Column(db.String(250), nullable=False, unique=True)
    location = db.Column(db.String(250), nullable=False)
    open = db.Column(db.String, nullable=False)
    close = db.Column(db.String, nullable=False)
    coffee_rating = db.Column(db.String, nullable=False)
    wifi_rating = db.Column(db.String, nullable=False)
    power = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Caffee {self.cafe}>'


with app.app_context():
    db.create_all()

# creates a form for user to add a new cafe
class CafeForm(FlaskForm):
    # creates all fields for the form
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe Location on Google Maps (URL)', validators=[DataRequired(), URL()])
    open = StringField('Opening Time e.g. 8AM', validators=[DataRequired()])
    close = StringField('Closing Time e.g. 5:30PM', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating',
                                choices=[('☕️', '☕️'), ('☕️ ', '☕️ ☕️'), ('☕️', '☕️ ☕️ ☕️'),
                                         ('☕️', '☕️ ☕️ ☕️ ☕️'), ('☕️', '☕️ ☕️ ☕️ ☕️ ☕️')],
                                validators=[DataRequired()])
    wifi_rating = SelectField('Wifi Strength Rating',
                              choices=[('💪', '💪'), ('💪', '💪 💪'), ('💪', '💪 💪 💪'),
                                       ('💪', '💪 💪 💪 💪'), ('💪', '💪 💪 💪 💪 💪')],
                              validators=[DataRequired()])
    power = SelectField('Power Socket Availability',
                        choices=[('✘', '🔌'), ('🔌', '🔌 🔌'), ('🔌', '🔌 🔌 🔌'),
                                 ('🔌', '🔌 🔌 🔌 🔌'), ('🔌', '🔌 🔌 🔌 🔌 🔌')],
                        validators=[DataRequired()])
    submit = SubmitField('Submit')


# creates a form for user to delete a cafe
class DelForm(FlaskForm):
    # creates all fields for the form
    cafe = StringField('Cafe name', validators=[DataRequired()])
    submit = SubmitField('Submit')


# Returns Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Adds new cafe to the file csv
@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    # Checks if form is submitted
    if form.validate_on_submit():
        # Gets data from the form
        with app.app_context():
            new_cafe = Caffees(
                cafe=form.cafe.data,
                location=form.location.data,
                open=form.open.data,
                close=form.close.data,
                coffee_rating=form.coffee_rating.data,
                wifi_rating=form.wifi_rating.data,
                power=form.power.data)
            db.session.add(new_cafe)
            db.session.commit()

            # Redirects to the home page
        return redirect(url_for('cafes'))

    else:
        return render_template('add.html', form=form)


# Deletes cafe from the file
@app.route('/delete', methods=['GET', 'POST'])
def delete():

    # Creates form
    del_form = DelForm()
    # Checks if form is submitted
    if del_form.validate_on_submit():
        # Gets data from the form
        cafe_name = del_form.cafe.data
        with app.app_context():
            del_cafe = Caffees.query.filter_by(cafe=cafe_name).first()
            db.session.delete(del_cafe)
            db.session.commit()
        return redirect(url_for('cafes'))

    # Redirects to the home page
    return render_template('delete.html', form=del_form)


# Displays all the cafes
@app.route('/cafes')
def cafes():
    all_cafes = Caffees.query.all()
    if not all_cafes:
        return render_template('cafes.html', cafes=[])
    else:
        return render_template('cafes.html', cafes=all_cafes)


# Runs Main Function
if __name__ == '__main__':
    app.run(debug=True)


