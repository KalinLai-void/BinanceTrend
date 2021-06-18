#### 題目
（使用BINANCE交易所API）

#### 功能說明 
- ~~GUI介面（使用Tkinter）~~
- ~~顯示各虛擬貨幣的市場走向~~
  - ~~即時更新~~
- ~~查詢自己的電子錢包~~
- 套用Twitter API，去抓Twitter幣圈新聞（#hashtag）
- 當某虛擬貨幣盈虧超過+X%時，通知現在是賣出的好時機
  - 低於-Y%時，警告使用者
- 建立交易訂單

#### 開發動機 (這個服務對什麼人有用?)

#### Previous Work (網路上是否已有類似服務？若有請附網址. 你為何想自己寫一個？)

#### Structure Chart (Top-Down Design) 以及每個模組的功能說明.

#### Input/Output Interface (你的程式，會有哪些主要的功能頁面？請以若干使用情境，展示這些畫面間的關係)

#### References (參考文獻及網站)
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

#### 使用的套件
- python-binance (Unofficial)
  - https://github.com/sammchardy/python-binance
  - 作者集合[Binance official API](https://github.com/binance/binance-spot-api-docs)並自行開發許多好用的功能

- matplotlib
  - 讓使用者視覺化資料
  
- mplfinance
  - 繪製K線圖
  - 由於matplotlib.finance在Matplotlib 3已被遺棄，因此以此函式庫取代

#### 若你的程式碼中有什麼值得強調的內容, 例如這個專題如何與你的本科專業結合, 或是哪個小功能特別得到使用者的讚賞，也可在簡報中特別說明.

#### 遇到的問題串
1. 出現下列錯誤訊息的原因與解決方法：
   電腦的時間伺服器並未與網路時間伺服器同步，去時間設定同步一下即可。
    > binance.exceptions.BinanceAPIException: APIError(code=-1021): Timestamp for this request was 1000ms ahead of the server's time.
2. matplotlib/mplfinance 如果要使用中文，需改變為中文字形，否則會亂碼
   - 安裝自訂字形：
     - 可先用以下程式碼找出matplotlib的路徑
        ```python
        import matplotlib
        print(matplotlib.__file__)
        ```
        這邊會顯示到matplotlib/__init__.py檔案的路徑，我們需要到matplotlib資料夾下面，然後找到mpl-data\fonts\ttf這條路徑，再將字型檔(.ttf)丟入進去
     - 到\.matplotlib 刪除所有快取檔案
       - matplotlib會在第一次import時建立字型列表
       - 需到C:\Users\使用者名稱\.matplotlib\，刪除字型列表(fontList.json)
     - 可用以下語法查看目前的字型，找到前面安裝的字型就代表成功安裝了
        ```python
        import matplotlib.font_manager
        
        a = sorted([f.name for f in matplotlib.font_manager.fontManager.ttflist])

        for i in a:
          print(i)
        ```
   - 使用字型：在畫圖前的style設定指定字型
      ```python
      style = mpf.make_mpf_style(..., rc={"font.sans-serif" : "字型名稱"})
      ```
   - 參考自 https://pyecontech.com/2020/03/27/python_matplotlib_chinese/
3. 使用原本使用的程式碼會造成記憶體一直無限增加，python回收機制清不掉
   - 舊程式碼如下，問題點在於**after每呼叫一次，FigureCanvasTkAgg會一直產生出新物件並以grid方式繪製出來**（舊的並不會被移除），已試過destroy，但畫面會一閃一閃不太舒服
    ```python
    currentPrice = 0
    def showCandlestickChart(coinSymbol):
    global currentPrice, fig, ax
      currentPrice = get_price(coinSymbol, currentPrice)

      colors = mpf.make_marketcolors(up="tab:green", down="tab:red",
                                      wick={"up" : "green", "down" : "red"})

      style = mpf.make_mpf_style(marketcolors=colors, mavcolors=["yellow", "purple", "skyblue"])

      fig, ax = mpf.plot(getBinanceKLines_DataFame(coinSymbol), 
                          title=currentPrice, ylabel="Price",
                          type="candle", style=style, tight_layout=True, figratio=(5, 3),
                          mav=(7, 25, 99), volume=True, returnfig=True)
      
      plt.close('all') # close previous figures, to avoid memory leak

      canvas = FigureCanvasTkAgg(fig, master=candleFigCanvas)
      canvas.draw()
      canvas.get_tk_widget().grid(row=0, column=0)
      candleFigCanvas.after(1000, lambda:showCandlestickChart(coinSymbol))
      ax.clear()
    ```
    - 因為這段程式碼要做的是將K線圖即時繪製出來，因此可以使用matplotlib套件中的animation類別，使圖片動態更新，程式碼如下
      - 匯入套件
        ```python
        import matplotlib.animation as animation
        ```
      - 繪圖物件設定，並使用FigureCanvasTkAgg物件將用matplotlib繪製的圖顯示在tkinter的視窗上
        ```python
        colors = mpf.make_marketcolors(up="tab:green", down="tab:red", wick={"up" : "green", "down" : "red"})
        style = mpf.make_mpf_style(marketcolors=colors, mavcolors=["orange", "purple", "skyblue"])

        fig = mpf.figure(style=style, figsize=(10, 6))

        # 這邊在將兩張圖合併，讓他看起來是一張圖
        # ax = fig.add_axes([left,bottom,width,height])
        mainAx = fig.add_axes([0.1, 0.3, 0.85, 0.60])
        volumeAx = fig.add_axes([0.1, 0.15, 0.85, 0.2])
        mainAx.xaxis.set_visible(False)
        
        canvas = FigureCanvasTkAgg(fig, master=candleFigCanvas)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0)
        ani = animation.FuncAnimation(fig, showCandlestickChart, fargs=("BTCUSDT",), interval=1000) 
        # 事件綁定，每1000秒呼叫一次去繪製
        # frgs是要傳遞的參數表，如果綁定的事件需傳遞參數可加入這個設定
        ```
      - 綁定的繪圖事件
        ```python
        currentPrice = 0
        def showCandlestickChart(i, coinSymbol): # 設定接收一個參數coinSymbol (i是預設的參數)
            global currentPrice
            klines_df = getBinanceKLines_DataFame(coinSymbol)
            mainAx.clear()
            volumeAx.clear() # 為節省記憶體，將之前的紀錄清掉

            currentPrice = get_price(coinSymbol, currentPrice)
            # 繪圖
            mpf.plot(klines_df, ax=mainAx, volume=volumeAx, ylabel="Price", 
                          type="candle", style=style, mav=(7, 25, 99))
        ```
    