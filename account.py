import binanceAPI as BN_config
import data as BN_data 
from tkinter import *
import webbrowser

from decimal import Decimal

def sendToAPIConfig(keyE, passE):
    keyStr = keyE.get()
    passStr = passE.get()
    BN_config.writeAPIConfig(keyStr, passStr)
    BN_data.updateClient()

def setAPI():
    API_Settings = Toplevel()
    API_Settings.title("Binance API Settings")
    API_Settings.iconbitmap("icon\\API.ico")

    keyLabel = Label(API_Settings, text="API Key", font=("", 14, ""))
    secretLabel = Label(API_Settings, text="Secret Key", font=("", 14, ""))
    keyLabel.grid(row=0, column=0)
    secretLabel.grid(row=1, column=0)

    keyEntry = Entry(API_Settings, width=75, font=("", 14, ""))
    secretEntry = Entry(API_Settings, width=75, font=("", 14, ""))
    keyEntry.grid(row=0, column=1)
    secretEntry.grid(row=1, column=1)

    Button(API_Settings, text="Submit", font=("", 14,""), width=75, relief=GROOVE,
        command=lambda:sendToAPIConfig(keyEntry, secretEntry)).grid(row=2, column=0, columnspan=2)

    url = "https://www.binance.com/en-IN/support/faq/360002502072"
    Button(API_Settings, text="How to get Binance API?", font=("", 14,""), width=75, relief=GROOVE,
        command=lambda:webbrowser.open(url, new=1)).grid(row=3, column=0, columnspan=2)

    if BN_config.isConfigExisted(): # display API BN_config when Config is existed
        BN_config_dict = BN_config.getAPIConfig_dict()
        keyEntry.insert(0, BN_config_dict["API Key"])
        secretEntry.insert(0, BN_config_dict["Secret Key"])

###############################################################################################

coinDict = { } # to save account balances, key is asset
def setCoinListBox():
    global coinListBox
    for coin in BN_data.getAccountBalances():
        coinListBox.insert(END, coin["asset"])
        coinDict[coin["asset"]] = coin

def updateCoinListBox(event):
    global searchEntry
    searchTerm = searchEntry.get().upper().replace(" ", "")
    coinListBox.delete(0, END)
    coinDict.clear()
    
    if not searchTerm == "":
        for coin in BN_data.getAccountBalances():
            if searchTerm in coin["asset"]:
                coinListBox.insert(END, coin["asset"])    
                coinDict[coin["asset"]] = coin
    else:
        setCoinListBox()

def transferToUSDT(coin, total):
    # because BTC can be the most coins transfered
    # so we can transfer to BTC, then fransfer to USDT
    if coin == "USDT":
        usdt = total
    elif not coin == "BTC": # BTC isn't able to transfer itself
        to_btc = Decimal(BN_data.getPrice(coin+"BTC")) * total
        usdt = Decimal(BN_data.getPrice("BTCUSDT")) * to_btc
    else:
        usdt = Decimal(BN_data.getPrice("BTCUSDT")) * total
    
    return usdt

def setCoinListBoxSelection(index):
    global coinDataLabel_dict, coinDataFrame
    coin = coinDict[coinListBox.get(index)]
    for data in coin:
        if data == "asset":
            coinDataFrame.config(text=coin[data])
        else:
            text = data + ": " + coin[data]
            coinDataLabel_dict[data].config(text=text)
    
    # total price
    total = Decimal(coin["free"]) + Decimal(coin["locked"])
    
    to_usdt = transferToUSDT(coin["asset"], total)

    totalText = "total: " + "{}".format(total) + "\n"
    totalText += "( ≒ USDT${})".format(round(to_usdt, 2))
    coinDataLabel_dict["total"].config(text=totalText)

def onCoinListBoxSelected(event):
    obj = event.widget
    index = obj.curselection()
    setCoinListBoxSelection(index)

def getEquivalentUSDT():
    totalUSDT = 0
    for coin in BN_data.getAccountBalances():
        if Decimal(coin["free"]) > 0 or Decimal(coin["locked"]) > 0: # total > 0
            total = Decimal(coin["free"]) + Decimal(coin["locked"])
            totalUSDT += transferToUSDT(coin["asset"], total)

    return totalUSDT

def showOwned(): # only show owned coin
    global coinListBox, showMyOwned_var
    if showMyOwned_var.get() == 1:
        coinListBox.delete(0, END)
        coinDict.clear()
        for coin in BN_data.getAccountBalances():
            if Decimal(coin["free"]) > 0 or Decimal(coin["locked"]) > 0: # total > 0
                coinListBox.insert(END, coin["asset"])    
                coinDict[coin["asset"]] = coin
    elif showMyOwned_var.get() == 0:
        coinListBox.delete(0, END)
        coinDict.clear()
        setCoinListBox()

def openWallet():
    global coinListBox, searchEntry, showMyOwned_var
    global coinDataLabel_dict, coinDataFrame

    walletLvl = Toplevel()
    walletLvl.title("Wallet")
    walletLvl.iconbitmap("icon\\Wallet.ico")

    usdtFrame = Frame(walletLvl)
    usdtFrame.pack(side=TOP)
    Label(usdtFrame, justify=CENTER, font=("", 14,""), text="Total asset ≒ USDT$ ").pack(side=LEFT)
    Label(usdtFrame, justify=CENTER, font=("", 16,"underline"),
          text="{}".format(round(getEquivalentUSDT(), 2))).pack(side=LEFT)

    featureFrame = Frame(walletLvl)
    featureFrame.pack(side=TOP)

    # ------------------------------------------------------------------------------------- #

    panelFrame = Frame(featureFrame)
    panelFrame.pack(side=LEFT)
    
    showMyOwned_var = IntVar()
    showMyOwned_checkBtn = Checkbutton(panelFrame, text="Only show owned coins",
                            variable=showMyOwned_var, onvalue=1, offvalue=0,
                            command=showOwned)
    showMyOwned_checkBtn.grid(row=0, column=0)

    searchEntry = Entry(panelFrame, width=15, font=("", 14,""))
    searchEntry.bind("<KeyRelease>", updateCoinListBox)
    searchEntry.grid(row=1, column=0, pady=5)

    listFrame = Frame(panelFrame)
    listFrame.grid(row=2, column=0)

    scrollbar = Scrollbar(listFrame, orient=VERTICAL)
    coinListBox = Listbox(listFrame, height=10, width=15, font=("", 14, ""), yscrollcommand=scrollbar.set)
    scrollbar.config(command=coinListBox.yview)
    setCoinListBox()
    scrollbar.pack(side=RIGHT, fill=Y)
    coinListBox.pack(fill=BOTH, expand=True)

    # ------------------------------------------------------------------------------------- #

    coinDataFrame = LabelFrame(featureFrame, font=("", 16,"bold"))
    coinDataFrame.pack(side=LEFT, anchor=NW, fill=Y)

    coinDataLabel_dict = { }
    coinDataLabel_dict["free"] = Label(coinDataFrame, font=("", 14, ""))
    coinDataLabel_dict["locked"] = Label(coinDataFrame, font=("", 14, ""))
    coinDataLabel_dict["total"] = Label(coinDataFrame, font=("", 14, ""), justify=LEFT)

    coinDataLabel_dict["free"].pack(anchor=NW)
    coinDataLabel_dict["locked"].pack(anchor=NW)
    coinDataLabel_dict["total"].pack(anchor=NW)

    # ------------------------------------------------------------------------------------- #

    coinListBox.bind("<<ListboxSelect>>", onCoinListBoxSelected)
    coinListBox.selection_set(0)
    setCoinListBoxSelection(0) # default display BTC asset

###############################################################################################
    