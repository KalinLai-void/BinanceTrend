## Virtual currency trend form（using Binance's API）
This is the terminal project of the course "Window Program Design (using Python Tkinter)" in my college.
((( my English is not good, sorry...

### README.md Language
- [English](/README.md)
- [Tranditional Chinese](/README.zh-tw.md)

### Dev. Motivation
This year, I just delved into virtual currency, from mining to trading. And I usually use [Binance](https://www.binance.com/) as my main exchange. Although they already have own website and program, I have the terminal project to finish. In that case, I think I can challenge myself. I will add all the features which I think are important as an integrated winform application.

### Features 
- With Binance API.
- Support GUI (using Tkinter).
- Show the market trend of each currency-pairs in Binance.
  - **Instant update**
- Look up the self wallet in Binance.

### Structure Chart
![](./Structure%20Chart.png)

### Input/Output Interface
![](./IO%20Interface-1.png)
![](./IO%20Interface-2.png)

### Future Prospects
- I want to use Twitter API, to get some import hashtag in tweets. To anyalyze data.
- When the newest price break through moving average or have more ups and downs, system will notice user.
  - Maybe using Bot of LINE or Telegram. 
- Creating a trading order.

> I just list it out. If I have time, I will update these features.

### Using Modules
- python-binance (Unofficial)
  - https://github.com/sammchardy/python-binance
  - The author based on [Binance official API](https://github.com/binance/binance-spot-api-docs) to develop many useful functions.

- matplotlib
  - Visualize data
  
- mplfinance
  - Draw candlestick chart (K-Line chart).
  - Because matplotlib.finance was abandoned in Matplitlib 3, I use this module to replace.