import discord
from datetime import datetime 
import yfinance as yf
import os, sys

client = discord.Client()

TOKEN = os.environ["STOCK_BOT_TOKEN"]

VALID_PERIODS = ["1d","5d","1mo","3mo","6mo","1y","2y","5y","10y","ytd","max"]


def get_last_close(symbol):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period="5d")
    
    if len(todays_data) == 0:
        return None
    else:
        return round(todays_data['Close'][-2], 2)


def get_last_open(symbol, period):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period=period)
    
    if len(todays_data) == 0:
        return None
    else:
        return round(todays_data['Open'][0], 2)
    
    
def get_last_price(symbol, period):
    ticker = yf.Ticker(symbol)
    todays_data = ticker.history(period=period)
    
    if len(todays_data) == 0:
        return None
    else:
        return round(todays_data['Close'][0], 2)


def get_current_price(symbol):
    return get_last_price(symbol, "1d")


def calc_returns(info, last_price):
    shares, amount = info.split("@")
    
    try:
        amount = float(amount)
        shares = float(shares)
        price = float(last_price)
    except:
        return "Unparseable data, format must be int@float"
    
    if shares < 0:
        pnl = (amount*shares - price*shares)*-1
    else:
        pnl = (price*shares - amount*shares)
        
    return round(pnl, 2), round(100*pnl/(amount*abs(shares)), 2)


def stock_gen_msg(stock):
    
    return_msg = ""
    
    last_price = get_current_price(stock)
    open_price = get_last_close(stock)    
    
    if last_price is not None:
        return_msg += f'\nLast price on {stock}: {last_price}'
        return_msg += f'\nLast close on {stock}: {open_price}'
        return_msg += f'\n% Change: {round((last_price-open_price)/last_price * 100,2)}'
    else:
        return_msg += "\nInvalid ticker {stock}, please check"
    
    return return_msg
        

def help_str():
    
    help_str = """Usage guide for stock-bot: 
        \nUse !stonk {TICKER} to get the last price of the ticker
        \nUse !stonk {TICKER},{TICKER},..., for price info on multiple tickers
        \nUse !stonk {TICKER} shares@price to calculate your PnL against an amount of shares at a given price.
        \nExample usage: !stonk GME 420@69
        \nUse !stonk {TICKER} {PERIOD} to pull price from the period ago and calculate change in price since.  
        \nValid periods are as follows: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max 
        \nExample usage: !stonk GME 5d"""

    return help_str


@client.event
async def on_message(message):

    if message.content.startswith('!stonk'):
        channel = message.channel
        content = message.content
        split_contents = content.split()
        stock = split_contents[1]
        invalid = False
        
        if stock == "help":
            return_msg = help_str()
            invalid = True
        else:
            if "," in stock:
                stocks = stock.split(",")
            else:
                stocks = [stock]
            return_msg = ""
            for stock in stocks:
                return_msg += stock_gen_msg(stock)
        
        if not invalid and len(stocks)==1:
            if len(split_contents) > 2:
                last_price = get_current_price(stock)                
                if "@" in split_contents[2]:
                    pnl_data = split_contents[2]
                    returns, pct_returns = calc_returns(pnl_data, last_price)
                    return_msg += f"\nCurrent PnL on {pnl_data}: ${returns}"
                    return_msg += f"\nROI on position: {pct_returns}%"
                    
                if split_contents[2] in VALID_PERIODS:
                    period = split_contents[2]
                    first_price = get_last_price(stock, period)
                    return_msg += f"\nClosing Price {period} agos: {first_price}"
                    return_msg += f"\nChange in price: {last_price - first_price}"
                    return_msg += f"\n% Change in price: {round((last_price - first_price)/first_price*100 ,2)}%"

        await channel.send(return_msg)                   
         
client.run(TOKEN)
