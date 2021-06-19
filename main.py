import binanceAPI as BN_config
import data as BN_data
import account as BN_account

from tkinter import * 
from tkinter import ttk
import datetime as dt

import mplfinance as mpf
import matplotlib
from matplotlib import animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use("TkAgg")

colors = mpf.make_marketcolors(up="tab:green", down="tab:red", wick={"up" : "green", "down" : "red"})
style = mpf.make_mpf_style(marketcolors=colors, mavcolors=["orange", "purple", "blue"])
fig = mpf.figure(style=style, figsize=(8, 6))

# ax = fig.add_axes([left,bottom,width,height])
mainAx = fig.add_axes([0.115, 0.33, 0.87, 0.63])
volumeAx = fig.add_axes([0.115, 0.15, 0.87, 0.15])
mainAx.xaxis.set_visible(False)

# add text, the position of left-bottom is (0, 0)
figtxts = [ fig.text(0.120, 0.97, "MA(7)", color="orange", size=12),
            fig.text(0.200, 0.97, "MA(25)", color="purple", size=12),
            fig.text(0.293, 0.97, "MA(99)", color="blue", size=12)  ]

selected_coinSymbol = None

###############################################################################################
def setCoinDataPanel():
    global fig, canvas
    global cycleComboList, priceLabel

    coinData_Fig_Frame = Frame(root)
    coinData_Fig_Frame.grid(row=1, column=1)

    priceLabel = Label(coinData_Fig_Frame, width=30, font=("", 14, "bold"))
    priceLabel.grid(row=0, column=0)

    cycleComboList = ttk.Combobox(coinData_Fig_Frame, state="readonly", width=10, font=("", 14,""))
    cycleComboList["values"] = ("1 Hour", "1 Day", "1 Week", "1 Month", "1 Year", "All history")
    cycleComboList.grid(row=0, column=1)
    cycleComboList.current(0)

    canvas = FigureCanvasTkAgg(fig, master=coinData_Fig_Frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0, columnspan=2)

def showCandlestickChart(i):
    selected_keepTime = cycleComboList.get()

    klines_df = BN_data.getBinanceKLines_DataFame(selected_coinSymbol, selected_keepTime)
    currentPrice = BN_data.getPrice(selected_coinSymbol)
    symbolsPair = list(BN_data.getMarket("ALL").keys())[list(BN_data.getMarket("ALL").values()).index(selected_coinSymbol)]
    # using the value to find the key in dictionary

    mainAx.clear()
    volumeAx.clear()
    
    priceLabel.config(text=symbolsPair + ": " + currentPrice)

    mav = ()
    figtxts[0].set_visible(False), figtxts[1].set_visible(False), figtxts[2].set_visible(False)

    if selected_keepTime == "1 Year" or selected_keepTime == "All history":
        mav = (7, 25, 99)
        figtxts[0].set_visible(True), figtxts[1].set_visible(True), figtxts[2].set_visible(True)
    elif selected_keepTime == "1 Month":
        mav = (7, 25)
        figtxts[0].set_visible(True), figtxts[1].set_visible(True)
    elif selected_keepTime == "1 Week":
        mav = (7)
        figtxts[0].set_visible(True)

    mpf.plot(klines_df, ax=mainAx, volume=volumeAx, ylabel="Price", 
                type="candle", style=style, mav=mav)

###############################################################################################
def setMarketListPanel():
    global selected_coinSymbol
    global searchEntry, coinListBox, ALL_Button, USDT_Button, BTC_Button, BNB_Button

    panelFrame = LabelFrame(root, text="Market Select", font=("", 16,"bold"))
    panelFrame.grid(row=0, column=0, rowspan=2)
    
    searchEntry = Entry(panelFrame, width=20, font=("", 14,""))
    searchEntry.bind("<KeyRelease>", updateCoinListBox)
    searchEntry.grid(row=0, column=0, columnspan=4, pady=5)

    ALL_Button = Button(panelFrame, text="ALL", font=("", 12,""), command=lambda:onMarketButtonClick("ALL"), relief=SUNKEN)
    USDT_Button = Button(panelFrame, text="USDT", font=("", 12,""), command=lambda:onMarketButtonClick("USDT"))
    BTC_Button = Button(panelFrame, text="BTC", font=("", 12,""), command=lambda:onMarketButtonClick("BTC"))
    BNB_Button = Button(panelFrame, text="BNB", font=("", 12,""), command=lambda:onMarketButtonClick("BNB"))

    ALL_Button.grid(row=1, column=0)
    USDT_Button.grid(row=1, column=1)
    BTC_Button.grid(row=1, column=2)
    BNB_Button.grid(row=1, column=3)

    listFrame = Frame(panelFrame)
    listFrame.grid(row=2, column=0, rowspan=2, columnspan=4)

    scrollbar = Scrollbar(listFrame, orient=VERTICAL)
    coinListBox = Listbox(listFrame, height=27, font=("", 14, ""), yscrollcommand=scrollbar.set)
    scrollbar.config(command=coinListBox.yview)
    setCoinListBox()
    scrollbar.pack(side=RIGHT, fill=Y)
    coinListBox.pack(fill=BOTH, expand=True)

    coinListBox.bind("<<ListboxSelect>>", onCoinListBoxSelected)
    coinListBox.select_set(0)
    selected_coinSymbol = BN_data.getMarket("ALL")[coinListBox.selection_get()]

def setCoinListBox():
    for cp in BN_data.getAllCoinPair().keys():
        coinListBox.insert(END, cp)

def updateCoinListBox(event):
    searchTerm = searchEntry.get().upper().replace(" ", "")
    searchPair = searchTerm.split('/') # avoid someone want to search xxx/yyy
    coinListBox.delete(0, END)
    
    if not searchTerm == "":
        ALL_Button.config(relief=RAISED)
        USDT_Button.config(relief=RAISED)
        BTC_Button.config(relief=RAISED)
        BNB_Button.config(relief=RAISED)

        for cp in BN_data.getAllCoinPair().keys():
            cp_slt = cp.split(' / ')
            if len(searchPair) > 1:
                if searchPair[0] in cp_slt[0] and searchPair[1] in cp_slt[1]:
                    coinListBox.insert(END, cp)
            else:
                if searchPair[0] in cp_slt[0]:
                    coinListBox.insert(END, cp)
    else:
        ALL_Button.config(relief=SUNKEN)
        setCoinListBox()
    
def onCoinListBoxSelected(event):
    global selected_coinSymbol
    try:
        obj = event.widget
        index = obj.curselection()
        selected_coinSymbol = BN_data.getMarket("ALL")[coinListBox.get(index)]
        cycleComboList.current(0)
    except:
        return

def onMarketButtonClick(coin):
    coinListBox.delete(0, END)
    ALL_Button.config(relief=RAISED)
    USDT_Button.config(relief=RAISED)
    BTC_Button.config(relief=RAISED)
    BNB_Button.config(relief=RAISED)
    
    if coin == "USDT":
        market = BN_data.getMarket("USDT")
        USDT_Button.config(relief=SUNKEN)
    elif coin == "BTC":
        market = BN_data.getMarket("BTC")
        BTC_Button.config(relief=SUNKEN)
    if coin == "BNB":
        market = BN_data.getMarket("BNB")
        BNB_Button.config(relief=SUNKEN)
    if coin == "ALL":
        market = BN_data.getMarket("ALL")
        ALL_Button.config(relief=SUNKEN)

    for ticker in market.keys():
        coinListBox.insert(END, ticker)
###############################################################################################

bIsAPISetted = False
def setMenu():
    global bIsAPISetted, accountMenu

    menuBar = Menu(root)
    root.config(menu=menuBar)

    accountMenu = Menu(menuBar)
    
    accountMenu.add_command(label="API Settings", command=BN_account.setAPI)
    
    if not BN_config.isConfigExisted():
        accountMenu.add_command(label="Wallet", command=BN_account.openWallet, state=DISABLED)
        bIsAPISetted = False
    else:
        accountMenu.add_command(label="Wallet", command=BN_account.openWallet, state=ACTIVE)
        bIsAPISetted = True

    menuBar.add_cascade(label="Account", menu=accountMenu)

def updateTitleClock_andDetectAPI():
    global bIsAPISetted, accountMenu
    now = dt.datetime.now()
    root.title("Binance 虛擬貨幣交易所 | " + now.strftime("%Y-%m-%d %H:%M:%S"))

    if not bIsAPISetted: 
        if BN_config.isConfigExisted():
            # only run 1 time
            BN_config.updateKeyAndSecret()
            BN_data.updateClient()
            accountMenu.entryconfigure(2, state=ACTIVE)
            bIsAPISetted = True

    root.after(200, updateTitleClock_andDetectAPI)

def onWinClosing():
    root.quit()
    root.destroy()

if __name__ == '__main__':
    root = Tk()
    root.iconbitmap("icon\\BINANCE_logo.ico")
    setMenu()
    updateTitleClock_andDetectAPI()

    # -------------------------------------------------------------- #
    setMarketListPanel()
    # -------------------------------------------------------------- #
    setCoinDataPanel()
    # -------------------------------------------------------------- #
    anim = animation.FuncAnimation(fig, showCandlestickChart, interval=1000)

    root.protocol("WM_DELETE_WINDOW", onWinClosing)
    root.mainloop()