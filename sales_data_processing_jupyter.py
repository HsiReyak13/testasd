# Sales Data Processing - Jupyter Notebook Single Cell
# This code consolidates all functionality into one cell for Jupyter notebook execution

import pandas as pd
import numpy as np
import os

# Configuration
input_file = "sales_data.csv"
output_file = "filtered_sales.csv"

print("Sales Data Processing Script")
print("="*50)

# Step 1: Load and inspect data
try:
    df = pd.read_csv(input_file)
    print(f"✓ Successfully loaded data from {input_file}")
    
    print("\n" + "="*50)
    print("DATA INSPECTION")
    print("="*50)
    
    print("\nFirst 5 rows:")
    print(df.head())
    
    print("\nDataFrame Info:")
    print(df.info())
    
    print("\nMissing values per column:")
    print(df.isnull().sum())
    
    print("\nData types:")
    print(df.dtypes)
    
except FileNotFoundError:
    print(f"✗ Error: File '{input_file}' not found.")
    raise
except pd.errors.EmptyDataError:
    print(f"✗ Error: File '{input_file}' is empty.")
    raise
except Exception as e:
    print(f"✗ Unexpected error loading file: {e}")
    raise

# Step 2: Clean data
print("\n" + "="*50)
print("DATA CLEANING")
print("="*50)

# Create a copy to avoid modifying the original
df_cleaned = df.copy()

# Check for missing values before cleaning
print("Missing values before cleaning:")
print(df_cleaned.isnull().sum())

# Fill missing Units_Sold with the column's mean
if 'Units_Sold' in df_cleaned.columns:
    units_sold_mean = df_cleaned['Units_Sold'].mean()
    missing_units = df_cleaned['Units_Sold'].isnull().sum()
    if missing_units > 0:
        df_cleaned['Units_Sold'] = df_cleaned['Units_Sold'].fillna(units_sold_mean)
        print(f"✓ Filled {missing_units} missing Units_Sold values with mean: {units_sold_mean:.2f}")

# Fill missing Revenue with 0
if 'Revenue' in df_cleaned.columns:
    missing_revenue = df_cleaned['Revenue'].isnull().sum()
    if missing_revenue > 0:
        df_cleaned['Revenue'] = df_cleaned['Revenue'].fillna(0)
        print(f"✓ Filled {missing_revenue} missing Revenue values with 0")

# Drop any rows where Product is missing
if 'Product' in df_cleaned.columns:
    missing_products = df_cleaned['Product'].isnull().sum()
    if missing_products > 0:
        df_cleaned.dropna(subset=['Product'], inplace=True)
        print(f"✓ Dropped {missing_products} rows with missing Product values")

print("\nMissing values after cleaning:")
print(df_cleaned.isnull().sum())

# Step 3: Filter and sort data
print("\n" + "="*50)
print("FILTERING AND SORTING")
print("="*50)

# Filter for Revenue > 1000
df_filtered = df_cleaned[df_cleaned['Revenue'] > 1000].copy()
print(f"✓ Filtered data: {len(df_filtered)} rows with Revenue > 1000 (from {len(df_cleaned)} total rows)")

# Sort by Revenue in descending order
df_final = df_filtered.sort_values('Revenue', ascending=False)
print("✓ Sorted data by Revenue in descending order")

print("\nFiltered and sorted data:")
print(df_final)

# Step 4: Save results
if len(df_final) == 0:
    print("\n⚠ Warning: No data meets the filtering criteria (Revenue > 1000)")
    print("Creating empty output file...")

try:
    df_final.to_csv(output_file, index=False)
    print(f"✓ Successfully saved filtered data to {output_file}")
    save_success = True
except Exception as e:
    print(f"✗ Error saving file: {e}")
    save_success = False

# Final summary
print("\n" + "="*50)
print("PROCESSING SUMMARY")
print("="*50)
print(f"Original rows: {len(df)}")
print(f"Cleaned rows: {len(df_cleaned)}")
print(f"Filtered rows (Revenue > 1000): {len(df_final)}")
print(f"Output file: {output_file}")

if save_success:
    print("✓ Data processing completed successfully!")
    
    # Verify the output file was created
    if os.path.exists(output_file):
        file_size = os.path.getsize(output_file)
        print(f"✓ Output file size: {file_size} bytes")
else:
    print("✗ Data processing failed during file save.")

# Display the final processed dataframe for Jupyter notebook
print("\n" + "="*50)
print("FINAL PROCESSED DATA")
print("="*50)
df_final