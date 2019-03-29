import inquirer_collect_news as icn
import rappler_collect_news as rcn
import numpy
import datetime
import pandas as pd
import generate_model


def start_collection():
    curr_year = datetime.date.today().year
    icn.start_inquirer()
    rcn.start_rappler()

    df1 = pd.read_csv("inquirer-"+str(curr_year)+".csv")
    df2 = pd.read_csv("rappler-"+str(curr_year)+".csv")
    main = pd.read_csv("main.csv")

    out = pd.concat([df1,df2]).drop_duplicates().reset_index(drop=True)
    out = pd.concat([out,main]).drop_duplicates(subset=['3'], keep='first').reset_index(drop=True)
    out.dropna(how='all', inplace = True)
    #out.sort_values(by=['2'], inplace=True, ascending=False)
        #temp = pd.read_csv("main.csv")
    with open('main.csv', 'w', encoding='utf-8') as f:
        out.to_csv(f, index=False)


    latest = (len(out) - len(main))
    if latest < 0:
        latest = latest * -1
        
    generate_model.main_with_clusters()
    temp = ""
    df_with_clusters = pd.read_csv("main_with_clusters.csv")
    for x in range(0, latest):
        temp += str(df_with_clusters['cluster'][x])+","

    k = temp.split(",")
    k.pop(-1)
    joined = ','.join(k)

    with open('latest.txt', 'w', encoding='utf-8') as txt:
         txt.write(joined)

    return latest


