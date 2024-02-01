from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)


class CafeForm(FlaskForm):
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


class DelForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv', 'a') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow([
                form.cafe.data,
                form.location.data,
                form.open.data,
                form.close.data,
                form.coffee_rating.data,
                form.wifi_rating.data,
                form.power.data])
        return redirect(url_for('cafes'))
    else:
        return render_template('add.html', form=form)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    del_form = DelForm()
    if del_form.validate_on_submit():
        cafe_name = del_form.cafe.data.strip().title()
        rows = []

        with open('cafe-data.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] != cafe_name:
                    rows.append(row)

        with open('cafe-data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        return redirect(url_for('cafes'))

    return render_template('delete.html', form=del_form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
