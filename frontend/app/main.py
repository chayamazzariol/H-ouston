"""
Frontend module for the Flask application.

This module defines a simple Flask application that serves
as the frontend for the project.
"""

from flask import Flask, render_template, request, jsonify, send_file
import requests  # Import the requests library to make HTTP requests
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, HiddenField, validators
import io

app = Flask(__name__)
# Replace with a secure secret key
app.config['SECRET_KEY'] = 'your_secret_key'

# Configuration for the FastAPI backend URL
# Replace with the actual URL of your FastAPI backend
FASTAPI_BACKEND_HOST = 'http://backend'
BACKEND_URL = f'{FASTAPI_BACKEND_HOST}/query/'


class QueryForm(FlaskForm):  # Class form for district name selection
    province_choices = [('Verona', 'Verona'), ('Vicenza', 'Vicenza'), ('Belluno', 'Belluno'), ('Treviso', 'Treviso'), ('Venezia', 'Venezia'), ('Padova', 'Padova'), ('Rovigo', 'Rovigo')]
    district_name = SelectField('District Name:', choices=([('', 'Select District')]+province_choices), validators=[validators.NoneOf('', 'Select District')])
    submit = SubmitField('Get Theaters from our Super Backend')


class CityQueryForm(FlaskForm):  # Class form for city name input
    city_name = StringField('City Name:')
    submit = SubmitField('Get Theaters from our Super Backend')


class CinemaQueryForm(FlaskForm):  # Class form for district name selection for statistics
    province_choices = [('Verona', 'Verona'), ('Vicenza', 'Vicenza'), ('Belluno', 'Belluno'), ('Treviso', 'Treviso'), ('Venezia', 'Venezia'), ('Padova', 'Padova'), ('Rovigo', 'Rovigo')]
    district_name = SelectField('District Name:', choices=([('', 'Select District')]+province_choices), validators=[validators.NoneOf('', 'Select District')])
    submit = SubmitField('Get statistics from our Super Backend')


class MyForm1(FlaskForm):
    dropdown_districts = SelectField('Select a District', choices=[], coerce=str)
    submit = SubmitField('Confirm District')
    reset = SubmitField('Reset')

    def set_choices(self, districts):
        self.dropdown_districts.choices = [(district[0], district[1]) for district in districts]


class MyForm2(FlaskForm):
    dropdown_cities = SelectField('Select a City', choices=[], coerce=str)
    submit = SubmitField('Confirm City')

    def set_choices(self, cities):
        self.dropdown_cities.choices = [(city[0], city[1]) for city in cities]


class MyForm3(FlaskForm):
    dropdown_theaters = SelectField('Select a Theater', choices=[], coerce=str)
    submit = SubmitField('Download Info')

    def set_choices(self, theaters):
        self.dropdown_theaters.choices = [(theater[0], theater[1]) for theater in theaters]


class DistrictQueryForm(FlaskForm):  # Class form for district name selection
    dis_name_cinema = StringField('District name:')
    submit = SubmitField('Get average capacity from our Super Backend')


@app.route('/')
def index():
    """
    Render the index page.

    Returns:
        str: Rendered HTML content for the index page.
    """
    # Fetch the date from the backend
    date_from_backend = fetch_date_from_backend()
    return render_template('index.html', date_from_backend=date_from_backend)


def fetch_date_from_backend():
    """
    Function to fetch the current date from the backend.

    Returns:
        str: Current date in ISO format.
    """
    # Adjust the URL based on your backend configuration
    backend_url = 'http://backend/get-date'
    try:
        response = requests.get(backend_url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json().get('date', 'Date not available')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching date from backend: {e}")
        return 'Date not available'


# Function 1
@app.route('/internal', methods=['GET', 'POST'])
def internal():
    """
    Render the internal page.

    Returns:
        str: Rendered HTML content for the index page.
    """
    form = QueryForm()
    district_theaters = None
    error_message = None  # Initialize error message

    if form.validate_on_submit():
        district_name = form.district_name.data

        # Make a GET request to the FastAPI backend
        fastapi_url = f'{FASTAPI_BACKEND_HOST}/district/{district_name}'
        response = requests.get(fastapi_url)
        print(response.content)

        if response.status_code == 200:
            # Extract and display the result from the FastAPI backend
            data = response.json()
            district_theaters = data.get('district_info', 'No data available')
            # result = data.get('city_info', f'Error: City not available for {city_name}')
            # return render_template('internal.html', form = form, result = result, error_message = error_message)
        else:
            error_message = f'Error: Unable to fetch City for {district_name} from our Super but limited Backend'

    return render_template('internal.html', form=form, district_theaters=district_theaters, error_message=error_message)


# Function 2
@app.route('/city', methods=['GET', 'POST'])
def city_query():
    """
    Render the city page.

    Returns:
        str: Rendered HTML content for the index page.
    """
    form = CityQueryForm()
    city_theaters = None
    error_message = None  # Initialize error message

    if form.validate_on_submit():
        city_name = form.city_name.data

        # Make a GET request to the FastAPI backend
        fastapi_url = f'{FASTAPI_BACKEND_HOST}/city/{city_name}'
        response = requests.get(fastapi_url)
        print(response.content)

        if response.status_code == 200:
            # Extract and display the result from the FastAPI backend
            data = response.json()
            city_theaters = data.get('city_info', 'No data available')
            # result = data.get('city_info', f'Error: City not available for {city_name}')
            # return render_template('internal.html', form = form, result = result, error_message = error_message)
        else:
            error_message = f'Error: Unable to fetch City for {city_name} from our Super but limited Backend'

    return render_template('city.html', form=form, city_theaters=city_theaters, error_message=error_message)


# Function 3
@app.route('/cinemastatistics', methods=['GET', 'POST'])
def district_query():
    """
    Render the cinemastatistics page.

    Returns:
        str: Rendered HTML content for the index page.
    """
    form = CinemaQueryForm()
    statistics = None
    error_message = None  # Initialize error message
    data = {}

    if form.validate_on_submit():
        district_name = form.district_name.data

        # Make a GET request to the FastAPI backend
        fastapi_url = f'{FASTAPI_BACKEND_HOST}/capacity_statistics/{district_name}'
        response = requests.get(fastapi_url)
        print(response.content)

        if response.status_code == 200:
            # Extract and display the result from the FastAPI backend
            data = response.json()
            statistics = data.get('district_name', 'No data available')
            # result = data.get('city_info', f'Error: City not available for {city_name}')
            # return render_template('internal.html', form = form, result = result, error_message = error_message)
        else:
            error_message = f'Error: Unable to fetch statistics for {district_name} from our Super but limited Backend'

    return render_template('cinemastatistics.html', form=form, statistics=data, error_message=error_message)


# Funzione 4
@app.route('/file', methods=['GET', 'POST'])
def download_file():
    districts = requests.post(f'{FASTAPI_BACKEND_HOST}/select_districts').json()
    form = MyForm1()
    form.set_choices(districts)
    print(form.dropdown_districts.choices)

    form2 = MyForm2()
    form3 = MyForm3()
    active_form = form

    if request.method == 'POST':
        if form.validate_on_submit() and form.submit.data:
            selected_district = request.form.get('dropdown_districts')
            form.set_choices([(selected_district, selected_district)])
            print(selected_district)
            cities = requests.post(f'{FASTAPI_BACKEND_HOST}/select_cities', data={"district": selected_district}).json()

            form2.set_choices(cities)
            print(cities)
            active_form = form2

            if form2.validate_on_submit() and form2.submit.data:
                selected_city = request.form.get('dropdown_cities')
                form2.set_choices([(selected_city, selected_city)])
                theaters = requests.post(f'{FASTAPI_BACKEND_HOST}/select_theater', data={"city": selected_city}).json()

                form3.set_choices(theaters)
                active_form = form3

                if form3.validate_on_submit() and form3.submit.data:
                    selected_option = form3.dropdown_theaters.data
                    form3.set_choices([(selected_option, selected_option)])
                    # Send POST request with selected option
                    response = requests.post(f'{FASTAPI_BACKEND_HOST}/download', data={"selected_option": selected_option, "district": selected_district, "city": selected_city})
                    print(response.content)
                    if response.status_code == 200:
                        # Convert response content to a file-like object
                        file_content = io.BytesIO(response.content)

                        # Return the file content for download
                        return send_file(file_content, as_attachment=True, download_name=f'{selected_option}.txt')
                    else:
                        return jsonify({"status": "error", "message": "File download failed"})

        elif form.reset.data:
            form.set_choices(districts)
            form2.set_choices([])
            form3.set_choices([])
            active_form = form
    return render_template('file.html', form=form, form2=form2, form3=form3, active_form=active_form)


# Funzione 5
@app.route('/cinema_district', methods=['GET', 'POST'])
def cinema_district_query():
    """
    Render the internal page.

    Returns:
        str: Rendered HTML content for the index page.
    """
    form = DistrictQueryForm()
    cinema_dis = None
    error_message = None  # Initialize error message

    if form.validate_on_submit():
        dis_name_cinema = form.dis_name_cinema.data

        # Make a GET request to the FastAPI backend
        fastapi_url = f'{FASTAPI_BACKEND_HOST}/district_cinema/{dis_name_cinema}'
        response = requests.get(fastapi_url)
        print(response.content)

        if response.status_code == 200:
            # Extract and display the result from the FastAPI backend
            data = response.json()
            cinema_dis = data.get('dis_info_cinema', 'No data available')
            # return render_template('internal.html', form = form, result = result, error_message = error_message)
        else:
            error_message = f'Error: Unable to fetch City for {dis_name_cinema} from our Super but limited Backend'

    return render_template('cinema_district.html', form=form, cinema_dis=cinema_dis, error_message=error_message)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
