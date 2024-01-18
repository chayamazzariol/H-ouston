import os
import sys
import unittest
from fastapi.testclient import TestClient
import pandas as pd
from datetime import datetime


# Add the project root to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Now you can do the relative import
from app.main import app, district, city
from app.mymodules.function import print_province_names

client = TestClient(app)
df = pd.read_csv('/app/app/data.csv', sep = ';')
# Converting all the numbers inside the dataframe as strings for JSON
df = df.astype(str)

df2 = pd.read_csv('/app/app/cinema.csv', sep = ';')

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "Veneto"}

def test_select_districts():

    # Make a request to the /select_districts endpoint
    response = client.post('/select_districts')

    # Assert the status code is 200 (OK)
    assert response.status_code == 200

    # Extract the expected result based on the mock data
    expected_result = [[district, district] for district in df['Provincia'].unique()]

    # Assert the response JSON matches the expected result
    assert response.json() == expected_result

def test_get_district():
    # Select a mock district for the request
    district_name = 'Verona'

    # Make a request to the /district/{district_name} endpoint
    response = client.get(f'/district/{district_name}')

    # Assert the status code is 200 (OK)
    assert response.status_code == 200

    # Extract the expected result based on the mock data and district_name
    dist_info = district(district_name, df)
    expected_result = {"district_name": district_name, "district_info": dist_info}

    # Assert the response JSON matches the expected result
    assert response.json() == expected_result

class TestPrintProvinceNames(unittest.TestCase):

    def setUp(self):
        # Create a temporary CSV file with sample data
        sample_data = {'Provincia': ['District1', 'District2', 'District3']}
        self.sample_df = pd.DataFrame(sample_data)
        self.tmp_csv_path = 'temp_data.csv'
        self.sample_df.to_csv(self.tmp_csv_path, sep=';', index=False)

    def tearDown(self):
        # Remove the temporary CSV file
        os.remove(self.tmp_csv_path)

    def test_print_province_names(self):
        # Mock the CSV file path in the function
        original_read_csv = pd.read_csv
        pd.read_csv = lambda path, sep: self.sample_df

        # Call the function
        result = print_province_names()

        # Restore the original read_csv function
        pd.read_csv = original_read_csv

        # Assert the result
        expected_result = "District1, District2, District3"
        self.assertEqual(result, expected_result)

def test_district(tmpdir):
    # Create a temporary CSV file with sample data
    sample_data = {'Provincia': ['District1', 'District2', 'District3']}
    sample_df = pd.DataFrame(sample_data)
    tmp_csv_path = os.path.join(tmpdir, 'data.csv')
    sample_df.to_csv(tmp_csv_path, sep=';', index=False)

    # Mock the CSV file path in the function
    original_read_csv = pd.read_csv
    pd.read_csv = lambda path, sep: sample_df

    # Call the function with a mock district_name
    mock_district_name = 'District2'
    result = district(mock_district_name, sample_df)

    # Restore the original read_csv function
    pd.read_csv = original_read_csv

    # Assert the result
    expected_result = {"district_name": mock_district_name, "district_info": sample_df[sample_df['Provincia'] == mock_district_name].to_dict(orient='records')}
    assert result == expected_result

def test_city(tmpdir):
    # Create a temporary CSV file with sample data
    sample_data = {'Città': ['City1', 'City2', 'City3']}
    sample_df = pd.DataFrame(sample_data)
    tmp_csv_path = os.path.join(tmpdir, 'data.csv')
    sample_df.to_csv(tmp_csv_path, sep=';', index=False)

    # Mock the CSV file path in the function
    original_read_csv = pd.read_csv
    pd.read_csv = lambda path, sep: sample_df

    # Call the function with a mock city_name
    mock_city_name = 'City2'
    result = city(mock_city_name, sample_df)

    # Restore the original read_csv function
    pd.read_csv = original_read_csv

    # Assert the result
    expected_result = {"city_name": mock_city_name, "city_info": sample_df[sample_df['Città'] == mock_city_name].to_dict(orient='records')}
    assert result == expected_result

def test_get_city():
    # Select a mock city for the request
    city_name = 'Villafranca di Verona'

    # Make a request to the /city/{city_name} endpoint
    response = client.get(f'/city/{city_name}')

    # Assert the status code is 200 (OK)
    assert response.status_code == 200

    # Extract the expected result based on the mock data and city_name
    city_info = city(city_name, df)  # Assuming you have a function 'city' to get city information
    expected_result = {"city_name": city_name, "city_info": city_info}

    # Assert the response JSON matches the expected result
    assert response.json() == expected_result

def test_download():
    # Select some mock data for the request
    selected_option = 'Auditorium Comunale'
    district = 'Verona'
    city = 'Villafranca di Verona'

    # Make a request to the /download endpoint
    response = client.post('/download', data={"selected_option": selected_option, "district": district, "city": city})

    # Assert the status code is 200 (OK)
    assert response.status_code == 200

    # Assert the content type of the response
    assert response.headers["content-type"] == 'application/octet-stream'

    # You may want to check the actual content of the file, but it might be sufficient to check if the file is non-empty
    assert len(response.content) > 0

    # Cleanup: Delete the temporary file created during the test
    os.remove(f"{selected_option}.txt")

def test_select_cities():
    # Select a mock district for the request
    district = 'Verona'

    # Make a request to the /select_cities endpoint
    response = client.post('/select_cities', data={"district": district})

    # Assert the status code is 200 (OK)
    assert response.status_code == 200

    # Extract the expected result based on the mock data
    filtered_df = df[df['Provincia'] == district]
    expected_result = [[city, city] for city in filtered_df['Città'].unique()]

    # Assert the response JSON matches the expected result
    assert response.json() == expected_result

def test_select_theater():
    # Select a mock city for the request
    mock_city = 'Villafranca di Verona'

    # Make a request to the /select_theater endpoint
    response = client.post('/select_theater', data={'city': mock_city})

    # Assert the status code is 200 (OK)
    assert response.status_code == 200

    # Extract the expected result based on the mock data and city
    filtered_df = df[df['Città'] == mock_city]
    theaters = list(filtered_df['Nome'].unique())
    expected_result = [[theater, theater] for theater in theaters]

    # Assert the response JSON matches the expected result
    assert response.json() == expected_result

def test_get_date():
    # Make a request to the /get-date endpoint
    response = client.get('/get-date')

    # Assert the status code is 200 (OK)
    assert response.status_code == 200

    # Extract the current date from the response JSON
    current_date_str = response.json()["date"]

    # Convert the current date string to a datetime object
    current_date = datetime.fromisoformat(current_date_str)

    # Assert that the current date is close to the expected date (within a small tolerance)
    assert abs((current_date - datetime.now()).total_seconds()) < 5
