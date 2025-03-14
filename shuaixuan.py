# Helena
# Date: 2024-03-22


import pandas as pd

# Load data from CSV file
def load_data(file_path):
    """
    Load financial data from a CSV file.
    
    Parameters:
    file_path (str): The path to the CSV file containing the data.
    
    Returns:
    DataFrame: A pandas DataFrame containing the loaded data.
    """
    try:
        data = pd.read_csv(file_path)
        print("Data loaded successfully.")
        return data
    except Exception as e:
        print(f"Failed to load data: {e}")
        return None

# Filter data based on income and savings criteria
def filter_data(data):
    """
    Filter the data to include only rows where income is greater than 7000 and savings is greater than 400.
    
    Parameters:
    data (DataFrame): The DataFrame containing the financial data.
    
    Returns:
    DataFrame: A DataFrame containing the filtered data.
    """
    try:
        filtered_data = data[(data['Income'] > 7000) & (data['Savings'] > 400)]
        print("Data filtered successfully.")
        return filtered_data
    except Exception as e:
        print(f"Failed to filter data: {e}")
        return None

# Save filtered data to a new CSV file
def save_data(filtered_data, output_file_path):
    """
    Save the filtered data to a new CSV file.
    
    Parameters:
    filtered_data (DataFrame): The DataFrame containing the filtered data.
    output_file_path (str): The path to the output CSV file.
    """
    try:
        filtered_data.to_csv(output_file_path, index=False)
        print(f"Filtered data saved to {output_file_path}")
    except Exception as e:
        print(f"Failed to save data: {e}")

# Main function to orchestrate the workflow
def main():
    # Define file paths
    input_file_path = 'data.csv'  # Replace with your actual input file path
    output_file_path = 'filtered_data.csv'  # Replace with your desired output file path
    
    # Load data
    data = load_data(input_file_path)
    
    # Filter data
    filtered_data = filter_data(data)
    
    # Save filtered data
    if filtered_data is not None:
        save_data(filtered_data, output_file_path)

# Run the main function
if __name__ == "__main__":
    main()