## 虛擬貨幣走勢分析（使用BINANCE交易所API）
此為大學課程「Python視窗程式設計」之期末專題

### Dev. Motivation
剛好今年開始接觸虛擬貨幣，從挖礦到買賣，而我一直常用的虛擬貨幣交易所是「[Binance幣安](https://www.binance.com/)」，雖然他們本身就有網站，但既然有期末專題，那我就當作挑戰自己，並且把我認為重要的功能都加入，做為一個整合式APP。

### Features 
- 串接Binance交易所的API
- GUI介面（使用Tkinter）
- 顯示各虛擬貨幣交易對的市場走向
  - **即時更新**
- 查詢自己的電子錢包

### Structure Chart
![](./Structure%20Chart.png)

### Input/Output Interface
![](./IO%20Interface-1.png)
![](./IO%20Interface-2.png)

### Future Prospects
- 套用Twitter API，去抓Twitter推文的hashtag，以便資料分析。
- 當突破均線，或者漲跌超過一定百分比，通知使用者。
  - 可能串接LINE Bot或Telegram。
- 建立交易訂單。

> 有機會再做，先列著xD

### Using Modules
- python-binance (Unofficial)
  - https://github.com/sammchardy/python-binance
  - 作者集合[Binance official API](https://github.com/binance/binance-spot-api-docs)並自行開發許多好用的功能

- matplotlib
  - 讓使用者視覺化資料
  
- mplfinance
  - 繪製K線圖
  - 由於matplotlib.finance在Matplotlib 3已被遺棄，因此以此函式庫取代

### References
- mplfinance使用方法
  - https://coderzcolumn.com/tutorials/data-science/candlestick-chart-in-python-mplfinance-plotly-bokeh
  - https://www.grenade.tw/blog/how-to-use-the-python-financial-analysis-visualization-module-mplfinance/

- 將matplotlib/mplfinance的圖表顯示在tkinter上
  - https://github.com/matplotlib/mplfinance/issues/304#issuecomment-751532329

- re正規表達式
  - https://docs.python.org/zh-tw/3/howto/regex.html
  - 分割虛擬貨幣Pair String的方法
    - https://code.luasoftware.com/tutorials/cryptocurrency/binance-split-trading-symbol/

- tkinter Combobox
  - https://docs.python.org/3.6/library/tkinter.ttk.html#combobox
  - https://www.pythontutorial.net/tkinter/tkinter-combobox/

- 使用entry搜尋，並更新相關選擇在listbox上（即時刷新）
  - https://youtu.be/0CXQ3bbBLVk

- Tkinter Menu & Toolbar
  - https://zetcode.com/tkinter/menustoolbars/

- Tkinter Checkbox
  - https://pythonbasics.org/tkinter-checkbox/