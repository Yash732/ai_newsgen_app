import yfinance as yf
from colorama import Fore
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "yfin-server",
    host = "0.0.0.0", port = 8000
    )

@mcp.tool()
def stock_info(stock_ticker: str)->str:
    """This tool returns information about a given stock given it's ticker.
    Args:
        stock_ticker: a alphanumeric stock ticker
        Example payload: "IBM"

    Returns:
        str:information about the company
        Example Respnse "Background information for IBM: {'address1': 'One New Orchard Road', 'city': 'Armonk', 'state': 'NY', 'zip': '10504', 'country': 'United States', 'phone': '914 499 1900', 'website': 
                'https://www.ibm.com', 'industry': 'Information Technology Services',... }" 
        """
    dat = yf.Ticker(stock_ticker)
    return str(f"Background information for {stock_ticker}: {dat.info}")

@mcp.tool()
def stock_price(stock_ticker: str)->str:
    """This tool returns the last known price for a given stock ticker.
    Args:
        stock_ticker: a alphanumeric stock ticker 
        Example payload: "NVDA"

    Returns:
        str:"Ticker: Last Price" 
        Example Respnse "NVDA: $100.21" 
        """
    dat = yf.Ticker(stock_ticker)
    historical_prices = dat.history(period = "1mo")

    last_months_close = historical_prices['Close']
    print(Fore.YELLOW + str(last_months_close))

    return str(f"Stock price over the last month for {stock_ticker}: {last_months_close}")

if __name__ == "__main__":
    mcp.run(transport = "streamable-http")