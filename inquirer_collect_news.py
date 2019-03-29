import requests
from bs4 import BeautifulSoup
import fileinput
import sys
import csv
import pandas as pd
from dateutil import parser
import datetime


def start_inquirer():
    print("Collecting Inquirer News...")
    not_this_year = 0
    curr_year = datetime.date.today().year
    f = open("data_inquirer.txt", "w")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36'
    }

    list1 = [] # News Title
    list2 = [] # News Content
    list3 = [] # News Date
    list4 = [] # News Links

    x = 1
    news_collected = 0
    while(not_this_year == 0):
        if (x == 1):
            page = requests.get("https://newsinfo.inquirer.net/tag/bicol", headers=headers)
        else:
            page = requests.get("https://newsinfo.inquirer.net/tag/bicol/page/"+str(x), headers=headers)

        soup = BeautifulSoup(page.text, 'lxml')
        soup.find('div', id="trending_side_wrap").extract()
        soup.find('div', id="channel-lbl").extract()

        date_soup = BeautifulSoup(page.text, 'lxml')
        date_soup.find('div', id="trending_side_wrap").extract()

        m = 0
        break_this = 0
        for date in date_soup.find_all('div', id="ch-postdate"): # Get the Date
            #date.find('span').extract()
            date_temp = (date.text).split("BY")[0]
            d = parser.parse(date_temp)
            if (str(curr_year) != str(d.year)):
                break_this = m + 1
                break
            m+=1
            #d = dt.datetime.strptime(str(date_temp), "%B %d, %Y")
            #print(d)
            list3.append(d)
            
        n = 0
        for h2 in soup.find_all('h2'):
            if (not_this_year != 0):
                break
            #print(h2.text+';')
            list1.append(h2.text)

            n+=1
            news_collected += 1
            f.write(h2.text+';')
            for a in h2.find_all('a', href=True):
                #break
                #print(a['href'])
                inner_page = requests.get(a['href'], headers=headers)
                inner_soup = BeautifulSoup(inner_page.text, 'lxml')
                #print(inner_soup)
                inner_soup.find('div', id="billboard_article").extract() #drop ads
                inner_soup.find('div', id="article_social_trending").extract()#drop trending
                inner_soup.find('h6').extract() #Drop h6

                #content = inner_soup.find_all('div',attrs={"id":"article_content"})
                #title = inner_soup.find("meta",  property="og:title", content=True)
                paragraph = inner_soup.find_all('p')

                #print(title.text)
                #print(paragraph.text)
                temp = ""
                for k in paragraph:
                    if ('INQUIRER PLUS' in k.text):
                        break
                    #print(k.text)
                    #list2.append(k.text)
                    temp+=k.text    
                    f.write(k.text)
                list4.append(a['href'])
                list2.append(temp)
            if ((n == break_this) and (break_this != 0)):
                not_this_year = 1
                break
        x+=1
        print("News Collected: ", news_collected)
                    
    df = pd.DataFrame(list(zip(*[list1, list2,list3,list4])))  #.add_prefix('Col')

    df.to_csv('inquirer-'+str(curr_year)+'.csv', index=False)
    print("Inquirer News Collection Complete")

    #with open('345.csv', 'wb') as csvfile:
    #        spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #        spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
    #        spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

    f.close()

    return news_collected
                   
