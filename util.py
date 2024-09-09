import os
import pandas as pd

def retrieve_data(stocks, dates, colname="Adj Close"):
    """Read stock data for given stocks from CSV files. Return an output
    dataframe.

    Parameters
    ----------
    stocks: list of stocks
    dates: period of data
    colname: name for columns

    Returns a dataframe.
    """    
    
    df = pd.DataFrame(index=dates)
    stocks = ["SPY"] + stocks
    base_dir = os.environ.get("MARKET_DATA_DIR", "csv/")
    
    # Iterate through the list of stocks to read data
    for stock in stocks:
        # File path for stock
        file_path = os.path.join(base_dir, f"{stock}.csv")

        # Import data for stock and drop na values
        df_temp = pd.read_csv(file_path, index_col="Date", parse_dates=True,
                          usecols=["Date", colname], na_values=["nan"])
            
        # Rename given column to stock title and add to dataframe
        df_temp.rename(columns={colname: stock}, inplace=True)
        df = df.join(df_temp)

        # Clean up empty data by removing empty rows from 'SPY' stock
        if stock == "SPY":
            df.dropna(subset=["SPY"], inplace=True)


    return df
