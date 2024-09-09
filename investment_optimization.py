import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as spo
from util import retrieve_data
import datetime as dt

def statistics(allocations, data):
    """Compute the cumulative return, mean daily return, standard deviation of
    the daily returns and sharpe ratio of the investment
    
    Parameters
    ----------
    allocations: Array where each cell is an allocation for a particular stock
    data: 2D array where each column is an independent stock

    I assume that the risk free rate is 0%.
    
    Returns the cumulative return, the mean of the daily returns, standard
    deviation of the daily returns, and sharpe ratio of entire investment
    portfolio
    """
    
    # Compute cumulative_return, daily_return_mean, daily_std, and sharpe_ratio
    daily_returns = data.pct_change().dropna()
    portfolio_returns = (daily_returns * allocations).sum(axis=1)
    cumulative_return = (portfolio_returns + 1).prod() - 1
    daily_return_mean = portfolio_returns.mean()
    daily_std = portfolio_returns.std()
    sharpe_ratio = (daily_return_mean / daily_std) * np.sqrt(252)
    
    return cumulative_return, daily_return_mean, daily_std, sharpe_ratio

def sharpe(allocations, data):
    """Function to compute the sharpe ratio based on stock data and allocations
    to each stock. Will go into the minimizer.

    Parameters
    ----------
    allocations: Array where each cell is an allocation for a particular stock
    data: 2D array where each column is an independent stock

    I assume that the risk free rate is 0%.

    Returns a sharpe ratio at the end.
    """

    # Compute Sharpe Ratio
    daily_returns = data.pct_change().dropna()
    portfolio_returns = (daily_returns * allocations).sum(axis=1)
    daily_return_mean = portfolio_returns.mean()
    daily_std = portfolio_returns.std()
    sharpe_ratio = (daily_return_mean / daily_std) * np.sqrt(252)
    
    return -sharpe_ratio

def investment_portfolio(start_date, end_date, stocks):
    """  		  	   		 	   		  		  		    	 		 		   		 		  
    This function generates a set of optimal allocations to maximize the
    associated Sharpe Ratio, for a set of stocks. This function will return the
    set of allocations, a cumulative return for the entire investment portfolio,
    sharpe ratio, an average daily return and a standard deviation of the daily
    return.
    
    Parameters
    ----------
    start_date: Start date		  	   		 	   		  		  		    	 		 		   		 		  
    end_date: End date		  	   		 	   		  		  		    	 		 		   		 		  
    stocks: Titles of stocks  		  	   		 	   		  		  		    	 		 		   		 		  
     		  	   		 	   		  		  		    	 		 		   		 		  
    Returns the allocations, sharpe ratio, cumulative return, average daily
    returns and standard deviation of daily returns		  		  		    	 		 		   		 		  
    """  		  	   		 	   		  		  		    	 		 		   		 		  
    
    # Import and modify SPY and stock csv data
    period = pd.date_range(start_date, end_date)
    all_data = retrieve_data(stocks, period) # data, including added SPY	    	 		 		   		 		  
    prices = all_data[stocks] # data, without SPY
    SPY_data = all_data["SPY"]  # SPY data 	   		  		  		    	 		 		   		 		  

    # Run the optimizer minimizer function to get the allocations
    beginning_allocs = [1/len(stocks)] * len(stocks)
    bound = [(0,1)] * len(stocks)
    constraint = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    temp_output = spo.minimize(sharpe, beginning_allocs, args=(prices,),
                               method='SLSQP', bounds=bound,
                               constraints=constraint, options={'disp': True})
    allocations = temp_output.x

    # Compile data
    cumul_return, daily_return, std, _sharpe = statistics(allocations, prices)
    normed_prices = prices/prices.iloc[0]
    normal_prices_allocated = normed_prices * allocations
    port_val = normal_prices_allocated.sum(axis=1) # Investment Portfolio data
    norm_SPY_data = SPY_data/SPY_data.iloc[0] # SPY data

    # Plot to compare investment portfolio with the S&P 500
    plt.figure(figsize=(10,6))
    plt.plot(port_val.index, port_val, label=f'Portfolio', color='black')
    plt.plot(norm_SPY_data.index, norm_SPY_data, label='SPY', color='blue')
    plt.xlabel('Date')
    plt.ylabel('Relative Price')
    plt.title('Investment Portfolio and SMP 500 over time')
    plt.legend()
    plt.grid(True)
    
    # Save plot
    plt.savefig('stock_comparison.png')
    
    # Export Data to Excel
    combined_data = pd.DataFrame({'Portfolio': port_val, 'SPY': norm_SPY_data})
    combined_data.to_excel('combined_data.xlsx', index=True)

    return allocations, _sharpe, cumul_return, daily_return, std  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
def main():  		  	   		 	   		  		  		    	 		 		   		 		  
    
    #Test case
    start_date = dt.datetime(2006, 1, 1)
    end_date = dt.datetime(2007, 1, 1)
    stocks = ["AMZN", "BEAM", "CBS", "CSCO", "EBAY"]
    allocations, cumul_return, sharpe, daily_return, std = investment_portfolio(
        start_date=start_date, end_date=end_date, stocks=stocks
    )  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
    # Print statistics  		  	   		 	   		  		  		    	 		 		   		 		  
    print(f'From {start_date} to {end_date}')
    print(f'Stocks: {stocks}')
    print(f'Allocations: {allocations}')
    print(f'Sharpe Ratio: {sharpe}')
    print(f'Standard Deviation: {std}')
    print(f'Daily Return: {daily_return}')
    print(f'Cumulative Return: {cumul_return}')

if __name__ == "__main__":  		  	   		 	   		  		  		    	 		 		   		 		  
    main()