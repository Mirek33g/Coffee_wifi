from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv


# Flask  Application Setup
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)


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
        with open('cafe-data.csv', 'a') as csv_file:
            # Writes data to the csv
            csv_writer = csv.writer(csv_file, delimiter=',')
            # Writes data to the csv
            csv_writer.writerow([
                form.cafe.data,
                form.location.data,
                form.open.data,
                form.close.data,
                form.coffee_rating.data,
                form.wifi_rating.data,
                form.power.data])
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
        cafe_name = del_form.cafe.data.strip().title()
        rows = []
        # Deletes data from the csv
        with open('cafe-data.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            # Writes data to the csv
            for row in reader:
                if row[0] != cafe_name:
                    rows.append(row)
        # Writes data to the csv
        with open('cafe-data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        # Redirects to the home page
        return redirect(url_for('cafes'))

    return render_template('delete.html', form=del_form)


# Displays all the cafes
@app.route('/cafes')
def cafes():
    # Gets data from the csv
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        # Writes data to the csv
        for row in csv_data:
            list_of_rows.append(row)
            # Redirects to the home page
    return render_template('cafes.html', cafes=list_of_rows)


# Runs Main Function
if __name__ == '__main__':
    app.run(debug=True)
