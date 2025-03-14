import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import socket

# Get the machine's hostname and IP address
hostname = socket.gethostname()  
ip_address = socket.gethostbyname(hostname)  

# Print the machine's hostname and IP address
print(f"Machine Name: {hostname}")
print(f"IP Address: {ip_address}")

# Load income data from an Excel file
income_df = pd.read_excel('income3.xlsx')
# Load expenses data from a text file
expenses_df = pd.read_csv('expenses3.txt', sep=' ')

# Convert the 'Month' column to string format for easier processing
income_df['Month'] = income_df['Month'].astype(str)
expenses_df['Month'] = expenses_df['Month'].astype(str)

# Convert the 'Month' column to datetime format
income_df['Month'] = pd.to_datetime(income_df['Month'].str.strip(), format='%Y-%m-%d', errors='coerce')
expenses_df['Month'] = pd.to_datetime(expenses_df['Month'].str.strip(), format='%Y-%m-%d', errors='coerce')

# Check for any invalid dates in the data
if income_df['Month'].isna().any():
    print("Warning: Invalid dates found in income data.")
if expenses_df['Month'].isna().any():
    print("Warning: Invalid dates found in expenses data.")

# Merge the income and expenses DataFrames on the 'Month' column
merged_df = pd.merge(income_df, expenses_df, on='Month', how='inner')

# Calculate savings by subtracting expenses from income
merged_df['Savings'] = merged_df['Income'] - merged_df['Expenses']

# Check for any logical errors in the data
if merged_df['Income'].sum() <= 0:
    raise ValueError("Total income must be greater than zero.")
if merged_df['Expenses'].sum() > merged_df['Income'].sum():
    raise ValueError("Total expenses cannot exceed total income.")

# Calculate the percentage of expenses relative to income
expense_percentage = merged_df['Expenses'].sum() / merged_df['Income'].sum() * 100
labels = ['Expenses', 'Savings']
sizes = [max(0, expense_percentage), max(0, 100 - expense_percentage)]

# Connect to an SQLite database and save the merged DataFrame
conn = sqlite3.connect('finance_data.db')
merged_df.to_sql('FinanceData', conn, if_exists='replace', index=False)

# Insert machine information into the database
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS MachineInfo (MachineName TEXT, IPAddress TEXT)''')
cursor.execute('''INSERT INTO MachineInfo (MachineName, IPAddress) VALUES (?, ?)''', (hostname, ip_address))
conn.commit()
conn.close()

# Create a figure with a specified size
plt.figure(figsize=(12, 6))

# Create a pie chart to show the distribution of expenses and savings
plt.subplot(1, 2, 1)
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
plt.title(f'Expense vs Savings Distribution\nMachine: {hostname} ({ip_address})')

# Create a line chart to show monthly savings trends
plt.subplot(1, 2, 2)
merged_df.sort_values('Month', inplace=True)
merged_df.set_index('Month')['Savings'].plot(kind='line', marker='o', color='green')
plt.title(f'Monthly Savings Trends\nMachine: {hostname} ({ip_address})')
plt.xlabel('Month')
plt.ylabel('Savings ($)')

# Adjust the layout to prevent overlap
plt.tight_layout()
# Display the plot
plt.show()
