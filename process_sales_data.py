#!/usr/bin/env python3
"""
Sales Data Processing Script

This script loads sales data from a CSV file, performs data cleaning by handling
missing values, filters data based on revenue conditions, sorts the results,
and saves the processed data to a new CSV file.

Author: Data Processing Script
Date: 2025-10-07
"""

import sys
import os
import subprocess
import importlib.util


def check_and_install_dependencies():
    """
    Check if required dependencies are installed and offer to install them if missing.
    
    Returns:
        bool: True if all dependencies are available, False otherwise
    """
    required_packages = {
        'pandas': 'pandas>=2.0.0',
        'numpy': 'numpy>=1.21.0'
    }
    
    missing_packages = []
    
    print("🔍 Checking required dependencies...")
    
    for package_name, pip_name in required_packages.items():
        try:
            spec = importlib.util.find_spec(package_name)
            if spec is not None:
                # Try to import to ensure it's working
                module = importlib.import_module(package_name)
                version = getattr(module, '__version__', 'unknown')
                print(f"✓ {package_name} {version} is available")
            else:
                missing_packages.append((package_name, pip_name))
                print(f"✗ {package_name} is not installed")
        except ImportError:
            missing_packages.append((package_name, pip_name))
            print(f"✗ {package_name} import failed")
    
    if not missing_packages:
        print("✅ All required dependencies are installed!")
        return True
    
    print(f"\n⚠ Missing {len(missing_packages)} required package(s):")
    for package_name, pip_name in missing_packages:
        print(f"   - {package_name}")
    
    print("\n📦 Installation options:")
    print("1. Install from requirements.txt (recommended):")
    print("   pip install -r requirements.txt")
    print("\n2. Install individual packages:")
    for package_name, pip_name in missing_packages:
        print(f"   pip install {pip_name}")
    print("\n3. Use the setup script:")
    print("   python setup.py install")
    
    # Ask user if they want to auto-install
    try:
        response = input("\n🤔 Would you like to automatically install missing packages? (y/N): ").strip().lower()
        if response in ['y', 'yes']:
            return auto_install_dependencies(missing_packages)
        else:
            print("\n❌ Cannot proceed without required dependencies.")
            print("Please install the missing packages and run the script again.")
            return False
    except (KeyboardInterrupt, EOFError):
        print("\n\n❌ Installation cancelled by user.")
        return False


def auto_install_dependencies(missing_packages):
    """
    Automatically install missing dependencies using pip.
    
    Args:
        missing_packages (list): List of tuples (package_name, pip_name)
    
    Returns:
        bool: True if installation successful, False otherwise
    """
    print("\n📦 Installing missing packages...")
    
    try:
        # First try to install from requirements.txt if it exists
        if os.path.exists('requirements.txt'):
            print("📋 Installing from requirements.txt...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
            ], capture_output=True, text=True, check=True)
            print("✅ Successfully installed packages from requirements.txt")
        else:
            # Install individual packages
            for package_name, pip_name in missing_packages:
                print(f"📦 Installing {package_name}...")
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", pip_name
                ], capture_output=True, text=True, check=True)
                print(f"✅ Successfully installed {package_name}")
        
        print("\n🔄 Verifying installation...")
        # Re-check dependencies
        all_installed = True
        for package_name, _ in missing_packages:
            try:
                importlib.import_module(package_name)
                print(f"✓ {package_name} is now available")
            except ImportError:
                print(f"✗ {package_name} installation verification failed")
                all_installed = False
        
        if all_installed:
            print("✅ All packages installed successfully!")
            return True
        else:
            print("❌ Some packages failed to install properly.")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        print("\n💡 Try installing manually:")
        print("   pip install -r requirements.txt")
        return False
    except FileNotFoundError:
        print("❌ pip command not found. Please ensure Python and pip are installed.")
        return False


# Check dependencies before importing pandas
if not check_and_install_dependencies():
    print("\n🚫 Exiting due to missing dependencies.")
    sys.exit(1)

# Now import pandas (should be available after dependency check)
try:
    import pandas as pd
    import numpy as np
except ImportError as e:
    print(f"❌ Failed to import required packages: {e}")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)


def load_data(filename):
    """
    Load data from CSV file with error handling.
    
    Args:
        filename (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: Loaded DataFrame or None if error occurs
    """
    try:
        df = pd.read_csv(filename)
        print(f"✓ Successfully loaded data from {filename}")
        return df
    except FileNotFoundError:
        print(f"✗ Error: File '{filename}' not found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"✗ Error: File '{filename}' is empty.")
        return None
    except pd.errors.ParserError as e:
        print(f"✗ Error parsing CSV file: {e}")
        return None
    except Exception as e:
        print(f"✗ Unexpected error loading file: {e}")
        return None


def inspect_data(df):
    """
    Display basic information about the DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame to inspect
    """
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


def clean_data(df):
    """
    Clean the DataFrame by handling missing values.
    
    Args:
        df (pd.DataFrame): DataFrame to clean
        
    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
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
    
    return df_cleaned


def filter_and_sort_data(df):
    """
    Filter data for Revenue > 1000 and sort by Revenue in descending order.
    
    Args:
        df (pd.DataFrame): DataFrame to filter and sort
        
    Returns:
        pd.DataFrame: Filtered and sorted DataFrame
    """
    print("\n" + "="*50)
    print("FILTERING AND SORTING")
    print("="*50)
    
    # Filter for Revenue > 1000
    filtered_df = df[df['Revenue'] > 1000].copy()
    print(f"✓ Filtered data: {len(filtered_df)} rows with Revenue > 1000 (from {len(df)} total rows)")
    
    # Sort by Revenue in descending order
    sorted_df = filtered_df.sort_values('Revenue', ascending=False)
    print("✓ Sorted data by Revenue in descending order")
    
    print("\nFiltered and sorted data:")
    print(sorted_df)
    
    return sorted_df


def save_data(df, filename):
    """
    Save DataFrame to CSV file with error handling.
    
    Args:
        df (pd.DataFrame): DataFrame to save
        filename (str): Output filename
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        df.to_csv(filename, index=False)
        print(f"✓ Successfully saved filtered data to {filename}")
        return True
    except PermissionError:
        print(f"✗ Error: Permission denied when trying to write to '{filename}'")
        return False
    except OSError as e:
        print(f"✗ Error: Could not write to file '{filename}': {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error saving file: {e}")
        return False


def main():
    """
    Main function that orchestrates the data processing workflow.
    """
    print("Sales Data Processing Script")
    print("="*50)
    
    # Define file paths
    input_file = "sales_data.csv"
    output_file = "filtered_sales.csv"
    
    # Step 1: Load and inspect data
    df = load_data(input_file)
    if df is None:
        print("Failed to load data. Exiting.")
        sys.exit(1)
    
    inspect_data(df)
    
    # Step 2: Clean data
    df_cleaned = clean_data(df)
    
    # Step 3: Filter and sort data
    df_filtered_sorted = filter_and_sort_data(df_cleaned)
    
    # Step 4: Save results
    if len(df_filtered_sorted) == 0:
        print("\n⚠ Warning: No data meets the filtering criteria (Revenue > 1000)")
        print("Creating empty output file...")
    
    success = save_data(df_filtered_sorted, output_file)
    
    # Final summary
    print("\n" + "="*50)
    print("PROCESSING SUMMARY")
    print("="*50)
    print(f"Original rows: {len(df)}")
    print(f"Cleaned rows: {len(df_cleaned)}")
    print(f"Filtered rows (Revenue > 1000): {len(df_filtered_sorted)}")
    print(f"Output file: {output_file}")
    
    if success:
        print("✓ Data processing completed successfully!")
        
        # Verify the output file was created
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"✓ Output file size: {file_size} bytes")
        
        return 0
    else:
        print("✗ Data processing failed during file save.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)