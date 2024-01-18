import pandas as pd


# Creating a string with districts' name from CSV file
def print_province_names():
    """
    Creating a string containing the districts' name that are in the data.csv
    """
    # Load CSV file
    df = pd.read_csv('/app/app/data.csv', sep=';')
    print("Find the theaters in these districts:")
    # Checking the existence of "District" column
    if 'Provincia' not in df.columns:
        return "The dataframe does not contain any 'District' column"
    # Extracting the districts' names from the DataFrame
    province_names = df['Provincia'].unique()
    # Creating a string with all the names
    names_str = ', '.join(province_names)
    return names_str
    result = print_province_names()
    print(result)


def district(district_name, df):
    """
    Endpoint to query information based on district_name.
    Args:
        district_name (str): The name of the district.
    Returns:
        district_info: Information for the provided district_name.
    """
    df = pd.read_csv('/app/app/data.csv', sep=';')
    # Converting all the numbers inside the dataframe as strings for JSON
    df = df.astype(str)
    # Convert district_name to title case for consistency
    district_name = district_name.title()
    # Check if the district_name exists in the 'name' column of the DataFrame
    if district_name in df['Provincia'].values:
        # Get rows where 'Provincia' is equal to district_name
        district_info = df[df['Provincia'] == district_name].to_dict(orient='records')
        for info in district_info:
            print(info)
        return {"district_name": district_name, "district_info": district_info}
    else:
        return {"Error": "District not found"}


def city(city_name, df):
    """
    Endpoint to query information based on city_name.
    Args:
        city_name (str): The name of the city.
    Returns:
        city_info: Information for the provided city_name.
    """
    df = pd.read_csv('/app/app/data.csv', sep=';')
    # Converting all the numbers inside the dataframe as strings for JSON
    df = df.astype(str)
    # Convert city name to title case for consistency
    city_name = city_name.title()
    # Check if the city_name exists in the 'name' column of the DataFrame
    if city_name in df['Città'].values:
        # Get rows where 'Città' is equal to city_name
        city_info = df[df['Città'] == city_name].to_dict(orient='records')
        for info in city_info:
            print(info)
        return {"city_name": city_name, "city_info": city_info}
    else:
        return {"Error": "City not found"}


def capacity_statistics(district_name, df2):
    """
    Calculating mean, maximum and minimum capacity for the cinemas of a given district
    """
    df2 = pd.read_csv('/app/app/cinema.csv', sep=';')
    # To select only the lines that regards CINEMA
    df_cinema1 = df2[df2['Genere locale'] == 'CINEMA']
    # To select only the lines that regards the cinemas of the chosen distric
    df_cinema = df_cinema1[df_cinema1['Provincia'] == (district_name.upper())]
    # Transforming 'Capienza' in integer
    df_cinema['Capienza'] = pd.to_numeric(df_cinema['Capienza'], errors='coerce')

    # Calculating statistics
    mean = (df_cinema['Capienza'].mean()).astype(str)
    # median = (df_cinema['Capienza'].median()).astype(str)
    maximum = (df_cinema['Capienza'].max()).astype(str)
    minimum = (df_cinema['Capienza'].min()).astype(str)
    return {'mean': mean, 'maximum': maximum, 'minimum': minimum}


def district_cinema(dis_name_cinema, df2):
    """
    Endpoint to query information based on dis_name_cinema.
    Args:
        dis_name_cinema (str): The name of the district.
    Returns:
        dis_info_cinema: Information for the provided dis_name_cinema.
    """
    df2 = pd.read_csv('/app/app/cinema.csv', sep=';')
    # To select only the lines that regards CINEMA
    df_cinema1 = df2[df2['Genere locale'] == 'CINEMA']
    # Converting all the numbers inside the dataframe as strings for JSON
    df_cinema = df_cinema1.astype(str)
    # Convert dis_name_cinema to uppercase case for consistency
    dis_name_cinema = dis_name_cinema.upper()
    # Check if the dis_name_cinema exists in the 'Provincia' column of the DataFrame
    if dis_name_cinema in df_cinema['Provincia'].values:
        # Get rows where 'Provincia' is equal to dis_name_cinema
        dis_info_cinema = df_cinema[df_cinema['Provincia'] == dis_name_cinema].to_dict(orient='records')
        for info in dis_info_cinema:
            print(info)
        return {"dis_name_cinema": dis_name_cinema, "dis_info_cinema": dis_info_cinema}
    else:
        return {"Error": "District not found"}
