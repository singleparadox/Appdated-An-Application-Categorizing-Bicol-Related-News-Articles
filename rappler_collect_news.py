import requests
from bs4 import BeautifulSoup
import fileinput
import sys
import csv
import pandas as pd
from dateutil import parser
import datetime
import re

def start_rappler():
    print("Collecting Rappler News...")
    not_this_year = 0
    curr_year = datetime.date.today().year
    f = open("rappler_data.txt", "w",encoding='utf-8')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36'
    }

    list1 = [] # News Title
    list2 = [] # News Content
    list3 = [] # News Date
    list4 = [] # News Link

    x = 1
    news_collected = 0
    while(not_this_year == 0):
        if (x == 1):
            page = requests.get("https://www.rappler.com/previous-articles?filterMeta=bicol", headers=headers)
        else:
            page = requests.get("https://www.rappler.com/previous-articles?filterMeta=bicol&start="+str((x-1)*50), headers=headers)

        soup = BeautifulSoup(page.text, 'lxml')
        #soup.find('div', id="trending_side_wrap").extract()
        #soup.find('div', id="channel-lbl").extract()

        date_soup = BeautifulSoup(page.text, 'lxml')
        #date_soup.find('div', id="trending_side_wrap").extract()

        '''for date in date_soup.find_all('div', id="ch-postdate"): # Get the Date
            #date.find('span').extract()
            date_temp = (date.text).split("BY:")[0]
            print(date_temp)
            list3.append(date_temp)'''
        
        m = 0
        break_this = 0
        for date in date_soup.find_all('span', class_="details"): # Get the Date
            #header = date_soup.find_all()
            date_temp = (date.text).split(" -")[0]

            d = parser.parse(date_temp)
            if (str(curr_year) != str(d.year)):
                break_this = m + 1
                break
            m+=1
            #d = parser.parse(date_temp)
            #print(d)
            list3.append(d)

        n = 0
        for h2 in soup.find_all('h3'):
            if ( (h2.text == 'Error') or (h2.text == 'Login') or (h2.text == 'Register for a RAPPLER Account') or (h2.text == 'Update your information')):
                break
            if ('thewrap' in h2):
                break
            if (not_this_year != 0):
                break
            #if (re.search('evening wrap', h2.text, re.IGNORECASE)):
            #    break
            #if (re.search('midday wrap', h2.text, re.IGNORECASE)):
            #    break
                
            #print(h2.text+';')
            list1.append(h2.text)
            n+=1
            news_collected += 1
            f.write(h2.text+';')

            for a in h2.find_all('a', href=True):
                #break
                #print(a['href'])
                inner_page = requests.get('http://www.rappler.com'+a['href'], headers=headers)
                #print('http://www.rappler.com'+a['href'])

                if ('the-wrap' in a['href']):
                    break
                    
                
                inner_soup = BeautifulSoup(inner_page.text, 'lxml')
                #print(inner_soup)
                #inner_soup.find('div', id="billboard_article").extract() #drop ads
                #inner_soup.find('div', id="article_social_trending").extract()#drop trending
                inner_soup.find('p', class_='caption').decompose() # Drop unnecessary mess
                inner_soup.find('div', id='askedition').decompose() # Sameflip-container
                inner_soup.find('div', class_='flip-container').decompose()
                inner_soup.find('div', id='userreg_modal').decompose()
                inner_soup.find('div', id='userlogin_modal').decompose()
                inner_soup.find('div', id='upd_thankyou').decompose()
                inner_soup.find('div', id='footer-wrapper').decompose()
                inner_soup.find('form', attrs={"role":""}).decompose()
                inner_soup.find('p', class_='details').decompose()
                
                #content = inner_soup.find_all('div',attrs={"id":"article_content"})
                #title = inner_soup.find("meta",  property="og:title", content=True)
                #paragraph = inner_soup.find_all('p', class_='p1')
                paragraph = inner_soup.find_all('p')

                #print(title.text)
                #print(paragraph.get_text())
                temp = ""
                for k in paragraph:
                    if ('Read More' in k.text):
                        break
                    #print(k.text)
                    #list2.append(k.text)
                    temp+=k.text    
                    f.write(k.text)
                list4.append("http://www.rappler.com"+a["href"])
                list2.append(temp)
            if ((n == break_this) and (break_this != 0)):
                not_this_year = 1
                break
        x+=1
        print("News Collected: ", news_collected)

    list1_temp = list1
    num = 0
    for i in list1_temp[:]:
        if ('Evening wRap' in i):
            del(list1[num])
            del(list2[num])
            del(list3[num])
            del(list4[num])
            #list2.pop(num)
            #list3.pop(num)
            num = num - 1    
        if ('Midday wRap' in i):
            del(list1[num])
            del(list2[num])
            del(list3[num])
            del(list4[num])
            #list2.pop(num)
            #list3.pop(num)
            num = num - 1
        '''if (re.search('(?<![\w])Evening wRap(?![\w])', i, re.IGNORECASE) is not None):
            print(i)
            del list1[num]
            del list2[num]
            del list3[num]
            #list2.pop(num)
            #list3.pop(num)
            num = num - 1    
        if (re.search('(?<![\w])Midday wRap(?![\w])', i, re.IGNORECASE) is not None):
            print(i)
            del list1[num]
            del list2[num]
            del list3[num]
            #list2.pop(num)
            #list3.pop(num)
            num = num - 1
        '''
        num+=1

    print("News Usable: ", len(list1))
                    
    df = pd.DataFrame(list(zip(*[list1, list2, list3, list4])))#   .add_prefix('Col')

    df.to_csv('rappler-'+str(curr_year)+'.csv', index=False)
    print("Rappler News Collection Complete")

    #with open('345.csv', 'wb') as csvfile:
    #        spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #        spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
    #        spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

    f.close()
    return len(list1)
