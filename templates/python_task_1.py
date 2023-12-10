import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here

    # Creating matrix based on id_1, id_2, car values
    df = df.pivot(index='id_1', columns='id_2', values='car')

    # Fill NaN values with 0
    df = df.fillna(0)

    # Set diagonal values of new_df to 0
    for i in df.index:
        for j in df.columns:
            if i == j:
                df.loc[i, j] = 0
                
    return df


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
        
    # Adding a new categorical column 'car_type' based on values of the 'car' column
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)

    # Calculate the count of occurrences for each 'car_type' category
    counts = df['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    counts = sorted(counts.items())
    
    return dict(counts)


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
        
    # Calculate the mean value of the 'bus' column
    bus_mean = df['bus'].mean()

    # Identify indices where the 'bus' values are greater than twice the mean
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()

    # Sort the indices in ascending order
    bus_indexes.sort()

    return list(bus_indexes)


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
        
    # Calculate the average of values in the 'truck' column for each route
    route_avg_truck = df.groupby('route')['truck'].mean()

    # Filter routes where the average of 'truck' values is greater than 7
    df = route_avg_truck[route_avg_truck > 7].index.tolist()

    # Sort the list of selected routes
    df.sort()

    return list()


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
        
    # Apply the specified logic to modify each value in the DataFrame
    matrix = matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)

    # Round the values to 1 decimal place
    matrix = matrix.round(1)

    return matrix


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here

    # Convert days to numerical representation
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df['startDay'] = df['startDay'].apply(lambda x: weekdays.index(x))
    df['endDay'] = df['endDay'].apply(lambda x: weekdays.index(x))

    # Convert start and end timestamps to datetime
    df['startTimestamp'] = df.apply(lambda row: convert_to_datetime(row, 'startTime', weekdays), axis=1)
    df['endTimestamp'] = df.apply(lambda row: convert_to_datetime(row, 'endTime', weekdays), axis=1)

    # Check if time range covers a full 24-hour period
    df['full_day_coverage'] = (df['endTimestamp'] - df['startTimestamp']) >= timedelta(hours=24)

    # Check if time range spans all 7 days of the week
    df['days_coverage'] = (df['endDay'] - df['startDay'] + 1) % 7 == 0

    # Group by id and id_2, check if any group has incorrect timestamps
    result = df.groupby(['id', 'id_2'])[['full_day_coverage', 'days_coverage']].all()
    
    return result
    
def convert_to_datetime(row, time_str, weekdays):
    day_str = weekdays[int(row['startDay'])]  # Convert back to string
    return datetime.strptime(day_str + ' ' + row[time_str], '%A %H:%M:%S')
