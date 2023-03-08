import pandas as pd
import logging

log = logging.getLogger('root')
DATE_COLS = ['order_date', 'ship_date']
CATEGORICAL_COLS = {
    "country": ['United States'],
    "segment": ['Consumer', 'Corporate', 'Home Office'],
    "category": ['Furniture', 'Office Supplies', 'Technology'],
    "ship_mode": ['Second Class', 'Standard Class', 'First Class', 'Same Day'],
    "region": ['South', 'West', 'Central', 'East']
}


def build_log(logger, message):
    logger(message, extra={'feature': 'TRANSFORM'})


def log_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            build_log(log.error,
                      f'Exception when applying {func.__name__}: {e}')
            raise Exception
    return wrapper


@log_errors
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
    build_log(log.info,
              'Renaming columns')
    return data.rename(columns=column_mapper)


@log_errors
def drop_index_column(data: pd.DataFrame):
    '''Drops the Row ID (row_id) column from the
    dataframe. It's purpuse can be replaced with the
    database ID, which will apply to all pipeline runs'''
    build_log(log.info,
              'Removing unnecessary columns (Row ID)')
    return data.drop(columns='row_id')


@log_errors
def drop_rows_with_missing_values(data: pd.DataFrame):
    '''Drop all rows with any missing value. For this
    scenario, it's considered that rows with just a single
    missing value in the record should be removed. Could
    be adjusted later according to business needs.'''
    initial_size = data.shape[0]
    build_log(log.info,
              f'Input data contains {initial_size} rows. Looking for rows with missing values')
    data_no_missing = data.dropna()

    final_size = data_no_missing.shape[0]
    missing = initial_size - final_size

    if initial_size == final_size:
        build_log(log.info,
                  f'No rows with missing values found. Continuing with {initial_size} rows.')
    else:
        build_log(log.warning,
                  f'Found and dropped {missing} rows. Continuing with {final_size} valid rows.')
    return data_no_missing


@log_errors
def convert_date_columns_to_datetime(data: pd.DataFrame):
    '''Columns with a date-like original value are
    converted to proper datetime objects.'''

    build_log(log.info,
              f'Changing type of {", ".join(DATE_COLS)} to datetime.')

    for col in DATE_COLS:
        data[col] = pd.to_datetime(data[col])
    return data


@log_errors
def get_year_from_datetime_cols(data: pd.DataFrame):
    '''Extract year dimension from datetime columns.'''

    build_log(log.info,
              f'Getting Year out of {", ".join(DATE_COLS)} columns.')

    for col in DATE_COLS:
        year_col = col.replace('date', 'year')
        data[year_col] = data[col].dt.year
    return data


@log_errors
def convert_categorical_cols_to_numeric(data: pd.DataFrame):
    '''Replaces categorical values with numerical values (from 0 to n
    categories) for columns that have low granularity (unique values < 10).
    Values outside of the defined expected ones will get a -1 value'''

    build_log(log.info,
              f'Encoding {", ".join(CATEGORICAL_COLS.keys())} columns to numbers.')

    def encoder(record, col_name, value_list):
        '''Tool to encode the category to number based on expected
        value list'''
        try:
            return value_list.index(record[col_name])
        except ValueError:
            return -1

    for col_name, expected_values in CATEGORICAL_COLS.items():
        data[col_name] = data.apply(encoder,
                                    axis=1,
                                    result_type='reduce',
                                    args=(col_name, expected_values))
    return data
