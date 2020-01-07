#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import codecs
import json
import tkinter as tk
import re
from tkinter import ttk
from tkinter import HORIZONTAL

def rutenAPI_Scraper(keyword, n_items):
    proc_array = []
    url1 = f'https://rtapi.ruten.com.tw/api/search/v3/index.php/core/prod?q={keyword}&type=direct&sort=rnk%2Fdc&offset=1&limit={n_items}&_callback=jsonpcb_CoreProd'
    #print(url1)
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url1,headers=headers)
    api1_data = BeautifulSoup(r.text,"html.parser")
    s_api1_data = str(api1_data)
    #print(s_api1_data)
    
    
    for i in range(n_items):
        index = s_api1_data.find("Id")
        #print(index)
        prodid = (s_api1_data[index+5:index+19])
        s_api1_data = s_api1_data[index+19:]
        
        url2 = f'https://rtapi.ruten.com.tw/api/prod/v2/index.php/prod?id={prodid}&bidway=all&_callback=jsonpcb_Prod'
        #print(url2)
        r = requests.get(url2,headers=headers)
        api2_data = BeautifulSoup(r.text,"html.parser")
        s_api2_data = str(api2_data)
        index1 = s_api2_data.find("ProdName")
        index2 = s_api2_data.find("SellerId")
        name = s_api2_data[index1+11:index2-3]
        #name.lstrip("\")
        #print(name)
        unicode_name = name.encode('utf8')
        name = (codecs.decode(unicode_name, 'unicode_escape'))
        
        index1 = s_api2_data.find("PriceRange")
        s_api2_data = s_api2_data[index1+13:]
        index1 = s_api2_data.find(',')
        price = s_api2_data[:index1]
        output = name + ':' + str(int(float(price)))
        proc_array.append(output)
    return proc_array
        #str_name = b(name).decode('unicode-escape')
        #print(str_name)
    """
    for i in range(n_items):
        prodid = api1_data['Rows'][i]['id']
        
        url2 = f'https://shopee.tw/api/v2/item/get?itemid={itemid}&shopid={shopid}'
        #print(url2)
        r = requests.get(url2,headers=headers)
        api2_data = json.loads(r.text)
        output = api1_data['items'][i]['name'] +':' + str(int((api2_data['item']['price'])/100000))
        proc_array.append(output)
    return proc_array
    """
    
def shopeeAPI_Scraper(keyword, n_items):
    proc_array = []
    url1 = f'https://shopee.tw/api/v2/search_items/?by=sales&page=0&keyword={keyword}'
    #print(url1)
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url1,headers=headers)
    api1_data = json.loads(r.text)
    
    for i in range(n_items):
        itemid = api1_data['items'][i]['itemid']
        shopid = api1_data['items'][i]['shopid']
        
        url2 = f'https://shopee.tw/api/v2/item/get?itemid={itemid}&shopid={shopid}'
        #print(url2)
        r = requests.get(url2,headers=headers)
        api2_data = json.loads(r.text)
        output = api1_data['items'][i]['name'] +':' + str(int((api2_data['item']['price'])/100000))
        proc_array.append(output)
    return proc_array

#shopeeAPI_Scraper(keyword = 'switch', n_items = 10)

def ruten_order(keyword, n_times):
    ruten_array = rutenAPI_Scraper(keyword, n_times)
    #pchome_array = pchomeAPI_Scraper(keyword, n_times)
    #print(len(shopee_array))
    ruten_item = []
    ruten_price = []
    for index1,n in enumerate(ruten_array):
        data = n.split(':')
        #print(index1)
        if(index1 == 0):
            #print(index1)
            ruten_item.append(data[0])
            ruten_price.append(data[1])
            continue
        combine = zip(ruten_item, ruten_price)
        count = 0
        for index2,x in enumerate(combine):
            """print('count: ',count)
            print('index2: ',index2)
            print('x: ',x[1])
            print('data: ',data[1])"""
            if(int(x[1]) > int(data[1])):
                #print("if 1")
                ruten_item.insert(index2, data[0])
                ruten_price.insert(index2, data[1])
                count = count+1
                break
            elif(index2+1 == len(ruten_item)):
                #print("if 2")
                ruten_item.append(data[0])
                ruten_price.append(data[1])
                count = count+1
                break
    result = zip(ruten_item,ruten_price)
    return list(result)
    #print(shopee_price)
    #print(shopee_item)
    

#ruten_order('switch',  6)

def pchomeAPI_Scraper(keyword, n_items):
    proc_array = []
    url1 = f'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q={keyword}&page=1&sortParm=rnk&sortOrder=dc'
    #print(url1)
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url1,headers=headers)
    api1_data = json.loads(r.text)
    
    for i in range(n_items):
        name = api1_data['prods'][i]['name']
        price = api1_data['prods'][i]['price']
        
        output = name + ':' + str(price)
        proc_array.append(output)
    return proc_array

#pchomeAPI_Scraper(keyword = 'switch', n_items = 10)

def shopee_order(keyword, n_times):
    shopee_array = shopeeAPI_Scraper(keyword, n_times)
    #pchome_array = pchomeAPI_Scraper(keyword, n_times)
    #print(len(shopee_array))
    shopee_item = []
    shopee_price = []
    for index1,n in enumerate(shopee_array):
        data = n.split(':')
        #print(index1)
        if(index1 == 0):
            #print(index1)
            shopee_item.append(data[0])
            shopee_price.append(data[1])
            continue
        combine = zip(shopee_item, shopee_price)
        count = 0
        for index2,x in enumerate(combine):
            """print('count: ',count)
            print('index2: ',index2)
            print('x: ',x[1])
            print('data: ',data[1])"""
            if(int(x[1]) > int(data[1])):
                #print("if 1")
                shopee_item.insert(index2, data[0])
                shopee_price.insert(index2, data[1])
                count = count+1
                break
            elif(index2+1 == len(shopee_item)):
                #print("if 2")
                shopee_item.append(data[0])
                shopee_price.append(data[1])
                count = count+1
                break
    result = zip(shopee_item,shopee_price)
    return list(result)
    #print(shopee_price)
    #print(shopee_item)
    

#shopee_order('switch',  6)

def pchome_order(keyword, n_times):
    #shopee_array = shopeeAPI_Scraper(keyword, n_times)
    pchome_array = pchomeAPI_Scraper(keyword, n_times)
    #print(len(shopee_array))
    pchome_item = []
    pchome_price = []
    for index1,n in enumerate(pchome_array):
        data = n.split(':')
        #print(index1)
        if(index1 == 0):
            #print(index1)
            pchome_item.append(data[0])
            pchome_price.append(data[1])
            continue
        combine = zip(pchome_item, pchome_price)
        count = 0
        for index2,x in enumerate(combine):
            """print('count: ',count)
            print('index2: ',index2)
            print('x: ',x[1])
            print('data: ',data[1])"""
            if(int(x[1]) > int(data[1])):
                #print("if 1")
                pchome_item.insert(index2, data[0])
                pchome_price.insert(index2, data[1])
                count = count+1
                break
            elif(index2+1 == len(pchome_item)):
                #print("if 2")
                pchome_item.append(data[0])
                pchome_price.append(data[1])
                count = count+1
                break
    #print(pchome_price)
    #print(pchome_item)
    result = zip(pchome_item,pchome_price)
    return list(result)

#pchome_order("switch", 5)

def combine_compare(keyword, n_times, model):
    #n_times = int(str_n_times)
    #model = int(str_model)
    pchome_best = pchome_order(keyword,n_times)
    shopee_best = shopee_order(keyword,n_times)
    ruten_best = ruten_order(keyword,n_times)
    #print(pchome_best[0])
    if(model == 1):
        if(int(pchome_best[0][1]) >= int(shopee_best[0][1]) and
          int(ruten_best[0][1]) >= int(shopee_best[0][1])):
            result = 'from shopee: ' + str(shopee_best[0])
            return result
        elif(int(shopee_best[0][1]) >= int(pchome_best[0][1]) and
          int(ruten_best[0][1]) >= int(pchome_best[0][1])):
            result = 'from pchome: ' + str(pchome_best[0])
            return result
        elif(int(pchome_best[0][1]) >= int(ruten_best[0][1]) and
          int(shopee_best[0][1]) >= int(ruten_best[0][1])):
            result = 'from ruten: ' + str(ruten_best[0])
            return result
    elif(model == 2):
        #result = ('all pchome: ' + str(pchome_best))
        result = 'all pchome: \n'
        for item in pchome_best:
            result = result + ('商品: ' + item[0] + '價錢: ' + item[1] + '\n') 
        return result
    elif(model == 3):
        #result = ('all shopee: ' + str(shopee_best))
        result = 'all shopee: \n'
        for item in shopee_best:
            result = result + ('商品: ' + item[0] + '價錢: ' + item[1] + '\n') 
        return result
    elif(model == 4):
        #result = ('all ruten: ' + str(ruten_best))
        result = 'all ruten: \n'
        for item in ruten_best:
            result = result + ('商品: ' + item[0] + '價錢: ' + item[1] + '\n') 
        return result


#allow non BMP unicode 
_nonbmp = re.compile(r'[\U00010000-\U0010FFFF]')

def _surrogatepair(match):
    char = match.group()
    assert ord(char) > 0xffff
    encoded = char.encode('utf-16-le')
    return (
        chr(int.from_bytes(encoded[:2], 'little')) + 
        chr(int.from_bytes(encoded[2:], 'little')))

def with_surrogates(text):
    return _nonbmp.sub(_surrogatepair, text)

def callbackFunc():
    resultString.set(with_surrogates(combine_compare(GoodsString.get(), int(LimitString.get()), int(ModelString.get()))))

#setting UI 
app = tk.Tk()
app.title('Welcome to easy shop')
app.geometry('600x600')

#image setting

def configitem():
    dict = {
        'imgA':tk.PhotoImage(file='welcome.gif'),
        'imgB':tk.PhotoImage(file='shopee.gif'),
        'imgC':tk.PhotoImage(file='pchome.gif'),
        'imgD':tk.PhotoImage(file='logo2.gif')
    }
    return dict

dict = configitem()
labelA = tk.Label(app,image=dict['imgA'])
labelA.grid(column=2, row=0, columnspan=2,sticky=tk.N)

"""
labelB = tk.Label(app,image=dict['imgB'])
labelB.grid(column=2, row=2, rowspan=2)

labelC = tk.Label(app,image=dict['imgC'])
labelC.grid(column=3, row=2, rowspan=2)
"""

labelD = tk.Label(app,image=dict['imgD'])
labelD.grid(column=2, row=2, rowspan=2, sticky=tk.E)

sh = ttk.Separator(app, orient=HORIZONTAL)
sh.grid(row=1,column=0,columnspan=5,sticky="we")

labelGoods = tk.Label(app, text = "商品名稱")
labelGoods.grid(column=1, row=2, sticky=tk.W)

labelLimit = tk.Label(app, text = "顯示數量")
labelLimit.grid(column=1, row=3, sticky=tk.W)

labelModel = tk.Label(app, text = "顯示模式")
labelModel.grid(column=1, row=4, sticky=tk.W)

ModelString = tk.StringVar()
r1 = tk.Radiobutton(app, text='顯示最便宜的商品',
                    variable=ModelString, value='1')
r1.grid(column=2, row=4, sticky=tk.W)
r2 = tk.Radiobutton(app, text='顯示所有pchome商品',
                    variable=ModelString, value='2')
r2.grid(column=2, row=5, sticky=tk.W)
r3 = tk.Radiobutton(app, text='顯示所有shopee的商品',
                    variable=ModelString, value='3')
r3.grid(column=2, row=6, sticky=tk.W)
r4 = tk.Radiobutton(app, text='顯示所有ruten的商品',
                    variable=ModelString, value='4')
r4.grid(column=2, row=7, sticky=tk.W)


GoodsString = tk.StringVar()
LimitString = tk.StringVar()
#ModelString = tk.StringVar()

entryGoods = tk.Entry(app, width=20, textvariable=GoodsString)
entryLimit = tk.Entry(app, width=20, textvariable=LimitString)
#entryModel = tk.Entry(app, width=20, textvariable=ModelString)

entryGoods.grid(column=2, row=2, sticky=tk.W)
entryLimit.grid(column=2, row=3, sticky=tk.W)
#entryModel.grid(column=2, row=3, padx=10)

resultButton = tk.Button(app, text = '顯示結果',
                         command=callbackFunc)
resultButton.grid(column=1, row=8, pady=10, sticky=tk.W)

resultString=tk.StringVar()
resultLabel = tk.Label(app, bg='Silver', textvariable=resultString)
resultLabel.grid(column=2, row=8, padx=10, sticky=tk.W)

"""
resultString = tk.StringVar()    
l = tk.Label(app, 
    textvariable=resultString,   
    bg='GhostWhite', font=('Arial', 12), width=120, height=30)
l.pack() 
"""
app.columnconfigure(2,weight=1)
#app.rowconfigure(0,weight=1)

app.mainloop()


# In[ ]:




