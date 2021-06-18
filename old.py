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