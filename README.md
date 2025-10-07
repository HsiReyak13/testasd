# Sales Data Processing Script

A Python script for processing sales data with data cleaning, filtering, and sorting capabilities.

## Features

- Load sales data from CSV files with robust error handling
- Data cleaning: handle missing values intelligently
- Filter data based on revenue conditions (Revenue > 1000)
- Sort results by revenue in descending order
- Save processed data to a new CSV file
- Comprehensive logging and progress reporting

## Installation

### Prerequisites

Make sure you have Python 3.7 or higher installed on your system.

### Install Dependencies

You can install the required dependencies using pip in several ways:

#### Option 1: Install from requirements.txt (Recommended)
```bash
pip install -r requirements.txt
```

#### Option 2: Install pandas directly
```bash
pip install pandas>=2.0.0
```

#### Option 3: Install with virtual environment (Best Practice)
```bash
# Create a virtual environment
python -m venv sales_env

# Activate the virtual environment
# On Windows:
sales_env\Scripts\activate
# On macOS/Linux:
source sales_env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Option 4: Install with pip upgrade
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Option 5: Quick installation scripts
```bash
# On Unix/Linux/macOS:
./install.sh

# On Windows:
install.bat

# Or use the comprehensive setup script:
python setup.py install
```

## Usage

1. **Prepare your data**: Place your sales data CSV file in the same directory as the script and name it `sales_data.csv`

2. **Run the script**:
   ```bash
   python process_sales_data.py
   ```

3. **Check the output**: The processed data will be saved as `filtered_sales.csv`

## Expected CSV Format

Your input CSV file should have the following columns:
- `Product`: Product name (required)
- `Units_Sold`: Number of units sold (missing values will be filled with mean)
- `Revenue`: Revenue amount (missing values will be filled with 0)

Example:
```csv
Product,Units_Sold,Revenue
Widget A,100,1500.00
Widget B,50,800.00
Widget C,200,2500.00
```

## Output

The script will:
1. Display data inspection information
2. Show data cleaning progress
3. Filter records with Revenue > 1000
4. Sort by Revenue (highest first)
5. Save results to `filtered_sales.csv`
6. Provide a processing summary

## Troubleshooting

### Common Installation Issues

If you encounter permission errors:
```bash
pip install --user -r requirements.txt
```

If you need to upgrade pip:
```bash
python -m pip install --upgrade pip
```

If pandas installation fails, try:
```bash
pip install --no-cache-dir pandas>=2.0.0
```

### Runtime Issues

- **File not found**: Ensure `sales_data.csv` exists in the same directory
- **Permission denied**: Check write permissions for the output directory
- **Memory issues**: For large files, consider processing in chunks

## Advanced Setup Options

### Using the Setup Script

The project includes a comprehensive setup script with multiple options:

```bash
# Install dependencies
python setup.py install

# Install with development dependencies
python setup.py dev

# Check if dependencies are installed
python setup.py check

# Create a virtual environment
python setup.py venv

# Clean installation files
python setup.py clean
```

### Automatic Dependency Management

The main script (`process_sales_data.py`) includes automatic dependency checking:
- Checks if required packages are installed when you run the script
- Offers to automatically install missing packages
- Provides clear installation instructions if dependencies are missing

## Development

### Installing Development Dependencies
```bash
# Using setup script (recommended)
python setup.py dev

# Or manually
pip install -r requirements.txt
pip install pytest flake8 black jupyter  # Optional: for testing and code formatting
```

### Running Tests
```bash
python -m pytest  # If you have tests
```

## License

This project is open source and available under the MIT License.
