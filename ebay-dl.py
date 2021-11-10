import argparse 
from bs4 import BeautifulSoup
import pandas as pd
import requests


def to_file(df, search, csv):
    name = ''
    k = 0
    for word in search:
        if k == 0:
            name = word
        else:
            name = name + '_' + word
        k += 1
    
    if csv:
        df.to_csv(name + '.csv', encoding='utf-8-sig', index = False)
    else:
        df.to_json(name + '.json', orient = 'records')
        



# set up parser
parser = argparse.ArgumentParser(description='Get products from ebay')
parser.add_argument('search', help='the search keyword for the desired product', default='xperia 1 iii')
parser.add_argument('--num', help='number of offers to download', type=int, default=3)
parser.add_argument('--csv', action='store_true', help='if present, saves the output as a csv rather than json filetype')
agrs = parser.parse_args()

print(agrs)

# get the search key words and split them by space
key_words = agrs.search.split()

# the base search url
search_url = r'https://www.ebay.com/sch/i.html?&_nkw='

# add key words to the url
for key_word in key_words:
    search_url = search_url + '+' + key_word

# desired number of outcomes per page
search_url = search_url + '&_ipg=' + str(agrs.num)

# get the results page
search_res = requests.get(search_url)

# load bs
soup = BeautifulSoup(search_res.content, 'html.parser')

offers = soup.find_all('a', class_='s-item__link', href=True)

offers_list = []
names_list = []

for offer in offers: 
    
    offers_list.append(offer['href'])    
    
    str_cells = str(offer)
    clean_text = BeautifulSoup(str_cells,"lxml").get_text()
    names_list.append(clean_text)

df_temp = pd.DataFrame({'name' : names_list, 'link' : offers_list})

df = pd.DataFrame(columns = ['name','price','status','shipping','free_returns','items_sold'])





i = 0
try:
    for each in range(agrs.num + 1):
        
        url = df_temp['link'][each]
        
        # get the result page
        search_res = requests.get(url)
        
        # load bs
        soup = BeautifulSoup(search_res.content, 'html.parser')
        
        #name
        try:
            name = soup.select('#itemTitle')
            item_name = name[0].get_text()
            item_name = item_name.lstrip('Details about').lstrip()
            #print('yay')
            i += 1

        except:
            continue
        
        #sales
        try:
            sold = soup.select('.vi-quantity-wrapper a')
            str_cells = str(sold[0])
            clean_text = BeautifulSoup(str_cells,"lxml").get_text()
            
            sales = int(clean_text[:clean_text.find(' ')])
            
        except:
            sales = 0
            
        #price
        try:
            price = soup.select('#prcIsum')
            dol_cen = price[0]['content'].split('.')

            dol = dol_cen[0]
            dol = dol.replace(',', '')
            cen = dol_cen[1]
            
            in_cents = int(dol)*100 + int(cen)

            
        except:
            try:
                price = soup.select('#prcIsum_bidPrice')
                dol_cen = price[0]['content'].split('.')

                dol = dol_cen[0]
                dol = dol.replace(',', '')
                cen = dol_cen[1]
                
                in_cents = int(dol)*100 + int(cen)                
            except:
                try:

                    price = soup.select('#mm-saleDscPrc')
                    dol_cen = price[0]['content'].split('.')

                    dol = dol_cen[0]
                    dol = dol.replace(',', '')
                    cen = dol_cen[1]
                    
                    in_cents = int(dol)*100 + int(cen) 
                except:
                    in_cents = None
            
            
         
        #condition
        try:
            cond = soup.findAll('div', {'itemprop':'itemCondition'})[0]
            condition = cond.get_text()
           
        except:
            condotion = None       
            
        #shipping
        shipping = 0
        try:
            ship = soup.select('#fshippingCost span')[0]
            ship_str = ship.get_text()
            if ship_str == 'FREE':
                shipping = 0
            else:
                ship_str = ship_str.lstrip('$')
                dol_cent_ship = ship_str.split('.')
                shipping = int(dol_cent_ship[0])*100 + int(dol_cent_ship[1])
            
        except:
            try:
                ship = soup.select('.sh_gr_bld_new')[0]
                if 'free' in ship.get_text().lower():
                    shipping = 0
            except:
                shipping = None
                
        #returns
        try:
            ret = soup.select('#vi-ret-accrd-txt')[0]

            ret = ret.get_text().lower()

            if 'free' in ret:
                returns = True

            else:
                returns = False
          
        except:
            returns = None 
       
        df = df.append({'name':item_name,'price':in_cents,'status':condition,'shipping':shipping,'free_returns':returns,'items_sold':sales}, ignore_index=True)        
        #print('name : ' + str(item_name) + '\nprice: ' + str(in_cents) + '\ncondition: ' + str(condition) + '\nshipping: ' + str(shipping) + '\nreturns: ' + str(returns) + '\nsales: ' + str(sales) + '\n\n')

        

except Exception as e: 
    print(e)
    print('There are probably fewer offers listed than you wanted. Saving %d offers.' %(i))
    to_file(df, key_words, agrs.csv)
    
to_file(df, key_words, agrs.csv)    
        
        

            
        
        
        
        
        
        
        
   