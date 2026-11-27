import csv

import pandas as pd


class InvalidDataError(Exception):
    """Error caused by an invalid data file"""


def get_behavior_columns(behavior_groups, dead_category):
    """
    List the behavior columns of all categories, except the dead category.

    Parameters:
    behavior_groups (dict): category name -> list of behavior columns.
    dead_category (str): name of the computed "dead" category, skipped.

    Returns:
    list: the behavior columns, in the order of the categories.
    """
    return [column for category, columns in behavior_groups.items()
            if category != dead_category
            for column in columns]


def load_coral_data(file_path):
    """
    Load coral data from a CSV file.

    Parameters:
    file_path (str): The path to the CSV file containing coral data.
    Both comma and semicolon separators are allowed.

    Returns:
    pd.DataFrame: A DataFrame containing the loaded coral data,
    with lower-case column names.
    """
    try:
        coral_data = pd.read_csv(file_path, sep=None, engine="python",
                                 encoding="utf-8-sig")
        coral_data.columns = coral_data.columns.str.lower()
        return coral_data

    except FileNotFoundError:
        raise InvalidDataError(f"The file at {file_path} was not found.")

    except pd.errors.EmptyDataError:
        raise InvalidDataError(f"The file at {file_path} is empty.")

    except pd.errors.ParserError:
        raise InvalidDataError("There was a parsing error while reading the file.")

    except csv.Error:
        raise InvalidDataError("Separator not detected or empty file")


def check_selection(dataframe, behavior_columns, default_behavior):
    """
    Warn about known behavior columns present in the file but not selected.

    Arguments:
    dataframe (pd.DataFrame): The DataFrame containing the data
    behavior_columns (list): list of selected behavior columns
    default_behavior (list): The default behavior columns

    Returns:
    Warning message to inform the user on column content.
    """
    warnings = []

    unselected_columns = [column for column in default_behavior
                          if column not in behavior_columns
                          and column in dataframe.columns]
    if unselected_columns:
        warnings.append(f"{', '.join(unselected_columns)} "
                        "is in your file but not selected for plotting: "
                        "these larvae will be counted as dead.")
    return warnings


def check_column_content(dataframe, mandatory_columns, default_behavior):
    """
    Check if the mandatory columns are present in the dataframe 
    and if there are additional columns

    Arguments:
    dataframe (pd.DataFrame): the dataframe containing the data
    mandatory_columns (list): list of mandatory columns
    default_behavior (list): The default behavior columns defined in config.py

    Returns:
    Warning message to inform the user on column content.

    Raises:
    InvalidDataError if mandatory column missing.
    """
    warnings = []
    missing_columns = [column for column in mandatory_columns
                       if column not in dataframe.columns]
    if missing_columns:
        raise InvalidDataError(f"Missing mandatory columns:"
                               f"{", ".join(missing_columns)}")

    additional_columns = [column for column in dataframe.columns
                          if column not in mandatory_columns and column not in default_behavior]
    if additional_columns:
        warnings.append(f"Additional columns detected: "
                        f"{", ".join(additional_columns)}.\n"
                        "These columns will be ignored.")
    return warnings


def prepare_data(coral_data,
                 mandatory_columns,
                 info_columns,
                 behavior_columns,
                 default_behavior,
                 total_larvae_column,
                 replicate_column):
    """
    Prepare the data to be plotted (check column content)

    Arguments:
    coral_data (pd.DataFrame): coral data DataFrame
    mandatory_columns (list): list of mandatory columns
    info_columns (list): list of info columns defined in config.py
    behavior_columns (list): list of selected behavior columns
    default_behavior (list): list of default behavior columns defined in config.py
    total_larvae_column (str): name of the column with total number of larvae in the replicate

    Returns:
    coral dataframe in shape to compute percentages + list of warnings

    Raises:
    InvalidDataError
    """
    warnings_list = []

    selection_check = check_selection(coral_data, behavior_columns, default_behavior)
    warnings_list.extend(selection_check)

    columns_check = check_column_content(coral_data, mandatory_columns, default_behavior)
    warnings_list.extend(columns_check)

    # Data preprocessing
    coral_data, warnings = data_preparation(coral_data,
                                            behavior_columns,
                                            info_columns + [replicate_column], 
                                            total_larvae_column)
    warnings_list.extend(warnings)

    return coral_data, warnings_list


def print_info_loaded_data(dataframe):
    """
    Print information about the loaded coral data.

    Parameters:
    dataframe (pd.DataFrame): The DataFrame containing the loaded data
    """
    if dataframe is not None:
        print(f"First 5 rows: \n{dataframe.head(5)}")
        print(f"{dataframe.shape[0]} rows and {dataframe.shape[1]} columns loaded successfully.")
        print("Table info:")
        dataframe.info()
        print(f"Column names: {dataframe.columns.tolist()}")
    else:
        print("No data to display. Please check the file path and ensure the file is not empty or corrupted.")


def data_preparation(dataframe, behavior_columns, id_columns, total_larvae_column):
    """
    Prepare the coral data for analysis.

    Parameters:
    dataframe (pd.DataFrame): The DataFrame containing the loaded data
    behavior_columns (list): Names of column for behavior data
    id_columns (list): Columns necessary to identify a row
    total_larvae_column (str): Name of the column with total number of larvae in the replicate

    What it does:
    Add a nb_dead column containing the number of dead larvae in the batch.
    Remove the rows where nb_dead < 0

    Returns:
    The updated dataframe and associated warnings when necessary.
    """
    warnings = []

    settled_larvae = dataframe[behavior_columns].sum(axis=1)
    dataframe["nb_dead"] = dataframe[total_larvae_column] - settled_larvae

    # Data check
    negative_dead_mask = dataframe["nb_dead"] < 0
    if negative_dead_mask.any():
        negative_dead_rows = dataframe.loc[negative_dead_mask, id_columns]
        negative_dead_rows_text = negative_dead_rows.to_string(index=False)
        warnings.append(
            f"{negative_dead_mask.sum()} rows were removed "
            f"because the number of dead larvae was negative:\n{negative_dead_rows_text}")

        # remove the problematic rows:
        dataframe = dataframe.drop(dataframe[negative_dead_mask].index)

    return dataframe, warnings