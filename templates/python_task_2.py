import pandas as pd


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    
    # Creating matrix based on id_start, id_end, distance values
    df = df.pivot_table(index='id_start', columns='id_end', values='distance', aggfunc='sum', fill_value=0)
    
    # Add values in Dataframe
    df = df.add(df.T, fill_value=0)
    
    # Set diagonal values to 0
    for i in df.index:
        for j in df.columns:
            if i == j:
                df.loc[i, j] = 0
                
    for i in range(len(df)-2):
        for j in range(len(df)-2-i):
            df.iloc[j+2+i,i] = df.iloc[j+1+i,i] + df.iloc[j+2+i,j+1+i]
            df.iloc[i,j+2+i] = df.iloc[j+2+i,i]

    return df


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    
    # Creating empty list for id_start, id_end, distance    
    id_start = []
    id_end = []
    distance = []

    # Adding values in the empty list
    for i in range(len(df.index)):
        for j in range(len(df.columns)):
            id_start.append(df.index[i])
            id_end.append(df.columns[j])
            distance.append(df.iloc[i,j])
            
    # Creating new dataframe     
    df = pd.DataFrame({'id_start':id_start,'id_end':id_end,'distance':distance})
    df = df[df['id_start'] != df['id_end']]
    
    return df


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here    
    
    # Filter DataFrame for the specified reference value
    reference_df = df[df['id_start'] == reference_value]

    # Calculate the average distance for the reference value
    reference_average_distance = reference_df['distance'].mean()

    # Calculate the lower and upper thresholds within 10%
    lower_threshold = reference_average_distance * 0.9
    upper_threshold = reference_average_distance * 1.1

    # Filter the DataFrame for values within the threshold
    within_threshold_df = df[(df['distance'] >= lower_threshold) & (df['distance'] <= upper_threshold)]

    # Get unique values from the id_start column and sort the list
    df = sorted(within_threshold_df['id_start'].unique())

    return df


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
        
    # Add columns for toll rates based on vehicle types
    df['moto'] = df['distance'] * 0.8
    df['car'] = df['distance'] * 1.2
    df['rv'] = df['distance'] * 1.5
    df['bus'] = df['distance'] * 2.2
    df['truck'] = df['distance'] * 3.6

    return df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
    
    # Convert start and end timestamps to datetime objects
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])

    # Extract day of the week, start time, and end time
    df['start_day'] = df['start_timestamp'].dt.day_name()
    df['start_time'] = df['start_timestamp'].dt.time
    df['end_day'] = df['end_timestamp'].dt.day_name()
    df['end_time'] = df['end_timestamp'].dt.time

    # Apply discount factors based on time ranges and weekdays/weekends
    weekday_discounts = {
        (datetime.time(0, 0, 0), datetime.time(10, 0, 0)): 0.8,
        (datetime.time(10, 0, 0), datetime.time(18, 0, 0)): 1.2,
        (datetime.time(18, 0, 0), datetime.time(23, 59, 59)): 0.8
    }

    weekend_discount = 0.7

    df['discount_factor'] = df.apply(lambda row: calculate_discount_factor(row), axis=1)

    # Apply discount factors to vehicle columns
    vehicle_columns = ['moto', 'car', 'rv', 'bus', 'truck']
    for col in vehicle_columns:
        df[col] = df[col] * df['discount_factor']

    # Drop temporary columns
    df = df.drop(['start_timestamp', 'end_timestamp', 'discount_factor'], axis=1)

    return df
