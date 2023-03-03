import pandas as pd


def standardize_column_names(data: pd.DataFrame):
    '''Reshapes the input dataframe so the columns
    labels are standardized'''
    column_mapper = {
        'Row ID': 'row_id',
        'Order ID': 'order_id',
        'Order Date': 'order_date',
        'Ship Date': 'ship_date',
        'Ship Mode': 'ship_mode',
        'Customer ID': 'customer_id',
        'Customer Name': 'customer_name',
        'Segment': 'segment',
        'Country': 'country',
        'City': 'city',
        'State': 'state',
        'Postal Code': 'postal_code',
        'Region': 'region',
        'Product ID': 'product_id',
        'Category': 'category',
        'Sub-Category': 'sub_category',
        'Product Name': 'product_name',
        'Sales': 'sales'
        }
    return data.rename(columns=column_mapper)


def drop_index_column(data: pd.DataFrame):
    '''Drops the Row ID (row_id) column from the
    dataframe. It's purpuse can be replaced with the
    database ID, which will apply to all pipeline runs'''
    return data.drop(columns='row_id')


def drop_rows_with_missing_values(data: pd.DataFrame):
    '''Drop all rows with any missing value. For this
    scenario, it's considered that rows with just a single
    missing value in the record should be removed. Could
    be adjusted later according to business needs.'''
    return data.dropna()


def convert_date_columns_to_datetime(data: pd.DataFrame):
    '''Columns with a date-like original value are
    converted to proper datetime objects.'''
    date_cols = ['order_date', 'ship_date']
    for col in date_cols:
        data[col] = pd.to_datetime(data[col])
    return data
