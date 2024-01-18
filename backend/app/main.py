"""
Backend module for the FastAPI application.

This module defines a FastAPI application that serves
as the backend for the project.
"""

from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, FileResponse
from datetime import datetime
import pandas as pd

from .mymodules.function import district, city, capacity_statistics, district_cinema

app = FastAPI()

df = pd.read_csv('/app/app/data.csv', sep=';')
# Converting all the numbers inside the dataframe as strings for JSON
df = df.astype(str)

df2 = pd.read_csv('/app/app/cinema.csv', sep=';')
# To select only the lines that regards CINEMA
df_cinema = df2[df2['Genere locale'] == 'CINEMA']


@app.get('/')
def read_root():
    """
    Root endpoint for the backend.

    Returns:
        dict: A simple greeting.
    """
    return {"Hello": "Veneto"}


# Create choices for SelectField
@app.post('/select_districts')
async def select_districts():
    # Extract unique city values from the filtered data
    districts = list(df['Provincia'].unique())
    # Create a list of tuples in the format [('Venezia', 'Venezia'), ...]
    result = [(district, district) for district in districts]

    return result


# Function 1
@app.get('/district/{district_name}')
def get_district(district_name: str):
    """
    if district_name in df['Provincia'].values:
        # Get rows where 'Provincia' is equal to district_name
        district_info = df[df['Provincia'] == district_name].to_dict(orient='records')
        print(district_info)
        return {"district_name": district_name, "district_info": district_info}
    else:
        return {"Error": "District not found"}
    """
    dist = district(district_name, df)
    return {"district_name": district_name, "district_info": dist}


# Function 2
@app.get('/city/{city_name}')
def get_city(city_name: str):
    """
    if city_name in df['Città'].values:
        # Get rows where 'Città' is equal to city_name
        city_info = df[df['Città'] == city_name].to_dict(orient='records')
        print(city_info)
        return {"city_name": city_name, "city_info": city_info}
    else:
        return {"Error": "City not found"}
    """
    cit = city(city_name, df)
    return {"city_name": city_name, "city_info": cit}


# Function 3
@app.get('/capacity_statistics/{district_name}')
def get_data(district_name: str):
    """
    calculating mean, median, maximum and minimum capacity for the cinemas in the csv file
    """
    data = capacity_statistics(district_name, df2)
    return {"district_name": district_name, 'mean': data["mean"], 'maximum': data["maximum"], 'minimum': data["minimum"]}


# Function 4
@app.post("/download")
async def download(selected_option: str = Form(...), district: str = Form(...), city: str = Form(...)):

    file_name = f"{selected_option}.txt"

    # Generate file content based on the selected option
    file_content = df[(df['Nome'] == selected_option) & (df['Provincia'] == district) & (df['Città'] == city)].to_csv(index=False).encode('utf-8')

    with open(file_name, 'wb') as file:
        # Write the content to the file
        file.write(file_content)

    # Return the file as a downloadable response
    return FileResponse(file_name, filename=file_name, media_type='application/octet-stream')


@app.post('/select_cities')
async def select_cities(district: str = Form(...)):
    # Filter the DataFrame based on the selected district
    filtered_df = df[df['Provincia'] == district]

    # Extract unique city values from the filtered data
    cities = list(filtered_df['Città'].unique())

    # Create a list of tuples in the format [('Venezia', 'Venezia'), ...]
    result = [(city, city) for city in cities]

    return result


@app.post('/select_theater')
async def select_theater(city: str = Form(...)):
    # Filter the DataFrame based on the selected district
    filtered_df = df[df['Città'] == city]

    # Extract unique city values from the filtered data
    theaters = list(filtered_df['Nome'].unique())

    # Create a list of tuples in the format [('Venezia', 'Venezia'), ...]
    result = [(theater, theater) for theater in theaters]

    return result


# Function 5
@app.get('/district_cinema/{dis_name_cinema}')
def get_district_cinema(dis_name_cinema: str):
    """
    if dis_name_cinema in df_cinema['Provincia'].values:
        # Get rows where 'Provincia' is equal to dis_name_cinema
        dis_info_cinema = df_cinema[df_cinema['Provincia'] == dis_name_cinema].to_dict(orient='records')
        print(dis_info_cinema)
        return {"dis_name_cinema": dis_name_cinema, "dis_info_cinema": dis_info_cinema}
    else:
        return {"Error": "District not found"}
    """
    dist = district_cinema(dis_name_cinema, df_cinema)
    return {"dis_name_cinema": dis_name_cinema, "dis_info_cinema": dist}


@app.get('/get-date')
def get_date():
    """
    Endpoint to get the current date.

    Returns:
        dict: Current date in ISO format.
    """
    current_date = datetime.now().isoformat()
    return JSONResponse(content={"date" : current_date})
