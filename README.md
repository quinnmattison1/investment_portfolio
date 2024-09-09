# Investment Portfolio Optimization

This python script creates an investment profile, with optimal allocations, to maximize the associated Sharpe Ratio. It uses historical stock data to calculate the cumulative return, mean daily return, standard deviation, and Sharpe ratio, and compares the investment portfolio's performance to the S&P 500.

There are several selections of data inside the 'data' file, including the 'SPY.csv' file for the S&P500.

## Features

- **Statistics Calculation**: Computes the cumulative return, mean daily return, standard deviation, and Sharpe ratio for a given set of stock allocations.
- **Sharpe Ratio Optimization**: Uses the `scipy.optimize` module to determine the optimal allocations for the largest Sharpe Ratio.
- **Data Visualization**: Plots and saves a comparison of the optimized portfolio's performance against the S&P 500.
- **Data Export**: Exports portfolio performance data to an Excel file.

## Usage

1. Install required packages:
pip install numpy pandas matplotlib scipy openpyxl

2. Run the script:

For Linux and macOS
PYTHONPATH="../:." python optimization.py

For Windows (PowerShell)
$env:PYTHONPATH="../;." ; python optimization.py

3. View the output
- The allocations, Sharpe ratio, daily returns and cumulative return are printed to the console.
- A plot that compares the allocated portfolio to the S&P500 is saved as stock_comparison.png
- A combined file of the portfolio and S&P500 data is exported to combined_data.xlsx.

## Requirements
- Python 3.x
- Libraries: numpy, pandas, matplotlib, scipy, openpyxl

The investment_optimization.py file automatically runs a test case consisting of the stocks ["AMZN", "BEAM", "CBS", "CSCO", "EBAY"] from 1/1/2006 to 1/1/2007.
