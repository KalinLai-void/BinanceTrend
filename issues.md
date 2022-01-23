### 遇到的問題串
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
    