import pandas as pd
from sqlalchemy import create_engine

# Define the fixed-width fields: (start, end) positions for each column (0-based, end exclusive)
colspecs = [(0, 10), (10, 20), (20, 30)]  # Example: adjust to your file's layout
column_names = ['field1', 'field2', 'field3']  # Example: adjust to your field names

# Read the fixed-width file
df = pd.read_fwf('your_file.txt', colspecs=colspecs, names=column_names, header=None)

# Create SQL Server connection string (adjust with your credentials)
engine = create_engine(
    'mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server'
)

# Write to SQL Server table (replace 'your_table' with your table name)
df.to_sql('your_table', engine, if_exists='append', index=False)