import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.optimize import minimize

class QuantitativeAnalysis:
    def __init__(self, stock_data):
        """
        Initialize the quantitative analysis with stock price data
        
        :param stock_data: DataFrame with 'Date' and 'Close' price columns
        """
        self.stock_data = stock_data
        
    def calculate_returns(self):
        """
        Calculate daily and cumulative returns
        
        :return: DataFrame with return calculations
        """
        # Calculate daily returns
        self.stock_data['Daily_Return'] = self.stock_data['Close'].pct_change()
        
        # Calculate cumulative returns
        self.stock_data['Cumulative_Return'] = (1 + self.stock_data['Daily_Return']).cumprod() - 1
        
        return self.stock_data
    
    def risk_analysis(self):
        """
        Perform basic risk analysis
        
        :return: Dictionary of risk metrics
        """
        daily_returns = self.stock_data['Daily_Return'].dropna()
        
        return {
            'mean_return': daily_returns.mean(),
            'std_dev': daily_returns.std(),
            'sharpe_ratio': daily_returns.mean() / daily_returns.std() * np.sqrt(252),  # Annualized
            'max_drawdown': self.calculate_max_drawdown()
        }
    
    def calculate_max_drawdown(self):
        """
        Calculate maximum drawdown
        
        :return: Maximum drawdown percentage
        """
        cumulative_returns = (1 + self.stock_data['Daily_Return']).cumprod()
        peak = cumulative_returns.cummax()
        drawdown = (cumulative_returns - peak) / peak
        return drawdown.min()
    
    def visualize_returns(self):
        """
        Create visualization of cumulative returns
        """
        plt.figure(figsize=(10, 6))
        plt.plot(self.stock_data['Date'], self.stock_data['Cumulative_Return'], label='Cumulative Returns')
        plt.title('Cumulative Returns Analysis')
        plt.xlabel('Date')
        plt.ylabel('Cumulative Return')
        plt.legend()
        plt.show()
    
    @staticmethod
    def monte_carlo_simulation(initial_price, days, mu, sigma, num_simulations=1000):
        """
        Perform Monte Carlo simulation for price predictions
        
        :param initial_price: Starting stock price
        :param days: Number of days to simulate
        :param mu: Mean return
        :param sigma: Standard deviation of returns
        :param num_simulations: Number of simulation runs
        :return: Numpy array of simulated price paths
        """
        # Generate random walks
        random_returns = np.random.normal(
            loc=mu/days, 
            scale=sigma/np.sqrt(days), 
            size=(num_simulations, days)
        )
        
        # Simulate price paths
        price_paths = initial_price * np.exp(np.cumsum(random_returns, axis=1))
        
        return price_paths

# Example usage
def main():
    # Generate sample stock data
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    prices = np.cumsum(np.random.normal(0.0005, 0.02, len(dates))) + 100
    stock_data = pd.DataFrame({
        'Date': dates,
        'Close': prices
    })
    
    # Create analysis instance
    quant_analysis = QuantitativeAnalysis(stock_data)
    
    # Calculate returns
    returns_data = quant_analysis.calculate_returns()
    
    # Perform risk analysis
    risk_metrics = quant_analysis.risk_analysis()
    print("Risk Metrics:", risk_metrics)
    
    # Visualize returns
    quant_analysis.visualize_returns()
    
    # Run Monte Carlo simulation
    initial_price = stock_data['Close'].iloc[-1]
    simulation_results = quant_analysis.monte_carlo_simulation(
        initial_price, 
        days=100, 
        mu=0.0005, 
        sigma=0.02
    )

if __name__ == "__main__":
    main()