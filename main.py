import requests
from flask import Flask, render_template, request, send_from_directory
from utils import bounding_box
from os import path, environ

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

api_key = environ.get('API_KEY')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':
        lat = request.form.get('lat')
        long = request.form.get('long')

        if not all([lat, long]):
            return {'status': 'error', 'message': 'latitude and longitude missing'}, 400

        if path.exists(f'geo_data/{lat}{long}.kml'):
            return {'status': 'success', 'message': 'file exists'}

        lat_min, lon_min, lat_max, lon_max = bounding_box(float(lat), float(long), 0.1)
        try:
            response = requests.get(
                f'https://opencellid.org/cell/getInArea?key={api_key}&BBOX={lat_min},{lon_min},{lat_max},{lon_max}')
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500

        with open(f'geo_data/{lat}{long}.kml', 'w') as f:
            f.write(response.text)
        return {'status': 'success', 'message': 'file created'}


@app.route('/geo/<path:filename>')
def send_file(filename):
    return send_from_directory('geo_data', filename)


if __name__ == '__main__':
    app.run(debug=True)
