from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import numpy as np
import json
import os


def save_output_in_json(output_file_path, data, data_description=''):
    """
    Saves data to a JSON file.

    Parameters:
        output_file_path (str): The path to the output JSON file.
        data (any): The data to be saved in the JSON file.
        data_description (str, optional): A description or key for the data (default: '').

    Returns:
        None

    Raises:
        ValueError: If the output file path is not provided.

    Example:
        output_file_path = 'output.json'
        data = {'key': 'value'}
        save_output_in_json(output_file_path, data, data_description='my_data')
    """
    # Validate output file path
    if not output_file_path:
        raise ValueError("Output file path is required.")

    try:
        with open(output_file_path, 'w', encoding='utf8') as json_file:
            indent = 4  # Set the indentation level (optional)
            if data_description != '':
                json.dump({data_description: data}, json_file, ensure_ascii=False, indent=indent, sort_keys=True)
            else:
                json.dump({'data': data}, json_file, ensure_ascii=False, indent=indent, sort_keys=True)
        print(f"JSON file '{output_file_path}' saved successfully!\n")
    except Exception as exc:
        print(f"!! Failed to save JSON file '{output_file_path}'. !!\n", exc)



def load_json_file(file_path):
    """
    Loads and returns the data from a JSON file.

    Parameters:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The loaded JSON data.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If the file contains invalid JSON.

    Example:
        file_path = 'data.json'
        data = load_json_file(file_path)
    """
    # Validate file existence
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"JSON file not found: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            data = json.load(file)
            print(f"JSON file '{file_path}' loaded successfully!\n")
            return data
    except json.JSONDecodeError as exc:
        raise json.JSONDecodeError(f"Failed to load JSON file '{file_path}': {exc}")
    except Exception as exc:
        raise Exception(f"Failed to load JSON file '{file_path}': {exc}")


def split_csv_into_multiple_csv(input_file, number_of_output_files):
    """
    Splits a CSV file into multiple separate CSV files based on the specified number of output files.

    Parameters:
        input_file (str): The path to the input CSV file.
        number_of_output_files (int): The desired number of output CSV files.

    Returns:
        None

    Raises:
        FileNotFoundError: If the input file does not exist.

    Example:
        input_file = 'data.csv'
        number_of_output_files = 3
        split_csv_into_multiple_csv(input_file, number_of_output_files)
    """
    # Validate input file existence
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    # Read the input CSV file
    df = pd.read_csv(input_file)

    # Calculate the split indexes
    split_indexes = np.int64(np.linspace(0, 1, number_of_output_files+1) * len(df))

    output_file_name, *file_format = input_file.split(".")
    file_format = file_format[-1] if file_format else ''

    # Splitting the DataFrame into separate CSV files
    for i, (start_idx, end_idx) in enumerate(zip(split_indexes, split_indexes[1:]), start=1):
        temp_df = df[start_idx:end_idx]
        temp_df.to_csv(f"{output_file_name}_{i}.{file_format}", index=False)
        print(f"{output_file_name}_{i}.{file_format} saved..")


def read_multiple_csv(files):
    """
    Reads multiple CSV files and combines them into a single DataFrame.

    Parameters:
        files (list): A list of file paths to the CSV files.

    Returns:
        pandas.DataFrame: A DataFrame containing the combined data from all CSV files.

    Raises:
        FileNotFoundError: If a file in the list does not exist.

    Example:
        files = ['data1.csv', 'data2.csv', 'data3.csv']
        combined_data = read_multiple_csv(files)
    """
    df_list = []

    def _read_csv(file):
        if not os.path.exists(file):
            raise FileNotFoundError(f"File not found: {file}")
        return pd.read_csv(file)

    with ThreadPoolExecutor() as executor:
        # Submit tasks to read CSV files concurrently
        futures = [executor.submit(_read_csv, file) for file in files]

        # Process results as they become available
        for future in futures:
            df = future.result()
            if len(df):
                df_list.append(df)

    # Concatenate the DataFrames
    combined_df = pd.concat(df_list, ignore_index=True)
    return combined_df


def split_csv_by_ratio_into_two_csv(input_file, output_file1, output_file2, split_ratio=0.5):
    """
    Splits a CSV file into two separate CSV files based on a split ratio.

    Parameters:
        input_file (str): The path to the input CSV file.
        output_file1 (str): The path to the first output CSV file.
        output_file2 (str): The path to the second output CSV file.
        split_ratio (float): The ratio at which to split the data (default: 0.5).

    Returns:
        None

    Raises:
        FileNotFoundError: If the input file does not exist.
        ValueError: If the split ratio is not within the valid range of 0 to 1.

    Example:
        input_file = 'data.csv'
        output_file1 = 'split1.csv'
        output_file2 = 'split2.csv'
        split_csv_by_ratio_into_two_csv(input_file, output_file1, output_file2, split_ratio=0.5)
    """
    
    # Validate input file existence
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Validate split ratio
    if not 0 <= split_ratio <= 1:
        raise ValueError("Split ratio must be between 0 and 1.")

    # Read the input CSV file
    df = pd.read_csv(input_file)
    
    # Calculate the split index
    split_index = int(len(df) * split_ratio)
    
    # Split the DataFrame into two parts
    df1 = df[:split_index]
    df2 = df[split_index:]
    
    # Write the split DataFrames to separate CSV files
    df1.to_csv(output_file1, index=False)
    df2.to_csv(output_file2, index=False)
    
    print("Splitting complete!")
