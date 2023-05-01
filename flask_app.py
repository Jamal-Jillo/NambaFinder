from oop import PhoneNumber
from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, SearchField
from wtforms.validators import DataRequired, Length
import secrets

app = Flask(__name__)
foo = secrets.token_urlsafe(16)
app.secret_key = foo

# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)
# Flask-WTF requires this line
csrf = CSRFProtect(app)


class PhoneNumberForm(FlaskForm):
    """Phone number form."""

    phone_number = SearchField('Phone Number', validators=[DataRequired(), Length(min=10, max=12)])
    submit = SubmitField('Search')


@app.route('/', methods=['GET', 'POST'])
def home():
    form = PhoneNumberForm()

    if form.validate_on_submit():
        try:
            number = PhoneNumber(form.phone_number.data)
            number.parse_number()
            number.validate_number()
            operator = number.lookup_operator()

            if operator:
                #flash(f'Phone number belongs to operator: {operator}')
                return render_template('result.html', operator=operator, form=form)
            else:
                flash('Operator not found')
        except ValueError as e:
            flash(str(e))

    return render_template('index.html', form=form)


@app.route('/result', methods=['GET'])
def result():
    return render_template('result.html')

@app.route('/operator', methods=['GET'])
def get_operator():
    # phone_number = request.args.get('phone_number')
    phone_number = PhoneNumberForm()
    try:
        number = PhoneNumber(phone_number)
        number.parse_number()
        number.validate_number()
        operator = number.lookup_operator()

        if operator:
            return jsonify({'operator': operator})
        else:
            return jsonify({'error': 'Operator not found'})
    except ValueError as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
