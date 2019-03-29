import tkinter as tk
import webbrowser
from importlib import reload
from time import sleep
from threading import Thread
import collect_news as cn
import os
import datetime
import generate_model
import json
from functools import partial
import pandas as pd
import numpy as np
import re
import calendar
import plot
import datetime as dt

class Application:   
    def __init__(self, master):
        category_button = {}
        notif_button = {}
        page_button = {}
        prev = 0
        next_ = 0
        def manual_collect_data():
            listbox.delete(0,tk.END)
            listbox.insert(0, "Collecting and analyzing news articles. This may take a while...")
            def inner_collect():
                x = cn.start_collection()
                listbox.insert(1, "Fetched News: "+str(x))
                listbox.insert(2, "Collection Finished!")
                #notif_dict[0].destroy()
                #notifications()
                reload(generate_model)
                generate_model.main_with_clusters()
                refresh_category_buttons()
                create_category_buttons()
            t2 = Thread(target=inner_collect) # Initialize Thread
            t2.start() # Start Thread

        def collect_data_scheduled():
            print("Collection Started")
            while(True):
                with open("sched.txt") as f:
                    text = f.read()
                    sched_time = json.loads(text)
                current_time = dt.datetime.now()
                hour = current_time.hour
                minute = current_time.minute
                sec = current_time.second
                print("Checking if time is "+ str(sched_time['hour'])+":"+ str(sched_time['minute'])+":"+ str(sched_time['second']))

                print(hour,minute,sec)

                if ( (hour == int(sched_time['hour'])) and (minute == int(sched_time['minute'])) ): # Check if it is midnight
                    print("Time is "+ str(sched_time['hour'])+":"+ str(sched_time['minute'])+", fetching news articles...") # Time is midnight
                    cn.start_collection()
                    #notif_dict[0].destroy()
                    #notifications()
                    reload(generate_model)
                    generate_model.main_with_clusters()
                    refresh_category_buttons()
                    create_category_buttons()
                sleep(15)
                
        def close_all():
            os._exit(1)

        def change_label_window():
            k = generate_model.kmeans.n_clusters
            inp_dict = []
            def edit_label ():
                diction = ""
                for x in range(0,len(inp_dict)):
                    categ_button_edit_text(str(inp_dict[x].get()), x)
                    if x == len(inp_dict)-1:
                        diction +=  "\""+str(x)+"\""+": \""+str(inp_dict[x].get()+"\"")
                    else:
                        diction +=  "\""+str(x)+"\""+": \""+str(inp_dict[x].get()+"\",")

                diction = "{"+diction+"}"
                with open("selected_model.txt") as f:
                    text = f.read()
                    a = text.strip()
                    file_name = os.path.basename(a)
                    no_extension = os.path.splitext(file_name)[0]
                if ( os.path.exists("cluster_labels/"+no_extension+".txt") == False ):               
                    with open("cluster_labels/"+no_extension+".txt",'w') as file:
                        file.write(diction)
                else:
                    with open("cluster_labels/"+no_extension+".txt",'w') as file:
                        file.write(diction) 
            
            window = tk.Toplevel(master)
            window.title('Change Labels')
            window.geometry("450x250")

            window_frame = tk.Frame(window, width=230, height=200)
            text_frame = tk.Frame(window, width=230, height=200, bg='red')
            
            
            window_frame.pack(side='left')
            text_frame.pack(side='right')
            for x in range(0, k):
                labelText = "Cluster "+str(x)+": "
                labelDir = tk.Label(window_frame, text=labelText)
                labelDir.grid(row=x,column=0)
                input_box = tk.Entry(window_frame)
                input_box.insert(0, "No Label")
                inp_dict.append(input_box)
                input_box.grid(row=x,column=1)

            submit_button = tk.Button(window_frame, text='Submit', command=edit_label)
            submit_button.grid(row=x+1, column=1)

            textbox = tk.Text(text_frame)

            cmc = generate_model.show_model_data()

            txt = ""
            for z in cmc:
                txt += z+"\n\n"

            textbox.insert(tk.END, txt)
            textbox.pack()
            

        def upload_model():
            def refresh_all():
                reload(generate_model)
                generate_model.main_with_clusters()
                with open("selected_model.txt") as f:
                    text = f.read()
                    a = text.strip()
                    file_name = os.path.basename(a)
                    no_extension = os.path.splitext(file_name)[0]
                if ( os.path.exists("cluster_labels/"+no_extension+".txt") == False ):
                    choice = tk.messagebox.askquestion("Question", "There are currently no labels set for this model, Would you like to set labels?", icon='warning')
                    if choice == 'yes':
                        change_label_window()
                refresh_category_buttons()
                create_category_buttons()
                listbox.delete(0,tk.END)
                listbox.insert(0, "Model Uploaded Successfully!")
                
            
            listbox.delete(0,tk.END)
            filename = tk.filedialog.askopenfilename()
            if filename == '': #If Cancel is clicked
                listbox.insert(0, "Operation Canceled...")
            else:
                listbox.insert(0, "Opening File...")
                #print('Selected:', filename)
                with open("selected_model.txt", "w") as text_file:
                    print(filename, file=text_file)
                
                t3 = Thread(target=refresh_all) # Initialize Thread
                t3.start() # Start Thread
                
                #for x in notif_dict:
                #    notif_dict[x].destroy()
                open("latest.txt", "w").close()
                #notif_dict[0] = tk.Label(notification_frame, text="There are no new notifications at this time...", foreground='red')
                #notif_dict[0].grid(row=1, column=0)
                

        def gen_model():
            def sub_btn():
                listbox.delete(0,tk.END)
                a = int(input_box_clus.get())
                mdl_name = generate_model.gen_model(a)
                listbox.insert(0, "New model generated at: "+mdl_name)
            window = tk.Toplevel(master)
            window.title('Generate Model')
            window.geometry("270x70")

            window_frame = tk.Frame(window)
            
            window_frame.grid(row=0,column=0)
            
            labelClus = "Number of Clusters: "
            labelClus_lbl = tk.Label(window_frame, text=labelClus)
            labelClus_lbl.grid(row=1,column=0)
            input_box_clus = tk.Entry(window_frame)
            input_box_clus.grid(row=1,column=1)

            submit_button = tk.Button(window_frame, text='Submit', command=sub_btn)
            submit_button.grid(row=3, column=1)

        def limit_view():
            def sub_btn():
                listbox.delete(0,tk.END)
                a = input_box_view.get()
                #mdl_name = generate_model.gen_model(a)
                with open("view.txt", "w") as file:
                    file.write(a)
                listbox.insert(0, "View limit set at: "+str(a))
            window = tk.Toplevel(master)
            window.title('Limit View')
            window.geometry("270x70")

            window_frame = tk.Frame(window)
            
            window_frame.grid(row=0,column=0)
            
            with open("view.txt", "r") as file:
                txt = file.read()
            print(txt)

            labelClus = "Please input the number of articles viewed per category (0 = unlimited) : "
            labelClus_lbl = tk.Label(window_frame, text=labelClus,wraplength=200)
            labelClus_lbl.grid(row=0,column=0)
            input_box_view = tk.Entry(window_frame)
            input_box_view.insert(0, txt)
            input_box_view.grid(row=1,column=0)

            submit_button = tk.Button(window_frame, text='Submit', command=sub_btn)
            submit_button.grid(row=1, column=1)

        def change_sched_time():
            def submit_data():
                listbox.delete(0,tk.END)
                if (input_hour.get() == ""):
                    h = 0
                else:
                    h = input_hour.get()
                if (input_minute.get() == ""):
                    m = 0
                else:
                    m = input_minute.get()
                if (input_second.get() == ""):
                    s = 0
                else:
                    s = input_second.get()

                with open("sched.txt", "w") as text_file:
                    print("{ \"hour\": \""+str(h)+"\", \"minute\": \""+str(m)+"\", \"second\": \""+str(s)+"\" }", file=text_file)

                current_time_set_label.config(text="Current time set: "+str(h)+":"+str(m)+":"+str(s))
                listbox.insert(0, "Time for scheduled collection is modified and saved...")
                listbox.insert(0, "New Schedule is "+str(h)+":"+str(m)+":"+str(s))

            with open("sched.txt") as f:
                text = f.read()
                sched_time = json.loads(text)

            window = tk.Toplevel(master)
            window.title('Change Scheduled Time')
            window.geometry("250x120")

            window_frame = tk.Frame(window)
            
            window_frame.grid(row=0,column=0)

            current_time_set_label = tk.Label(window_frame, text="Current time set: "+str(sched_time['hour'])+":"+str(sched_time['minute'])+":"+str(sched_time['second']))
            current_time_set_label.grid(row=0, column=0)
            
            label_hour_text = "Hour: "
            label_hour = tk.Label(window_frame, text=label_hour_text)
            label_hour.grid(row=2,column=0)
            input_hour = tk.Entry(window_frame)
            input_hour.grid(row=2,column=1)

            label_minute_text = "Minute: "
            label_minute = tk.Label(window_frame, text=label_minute_text)
            label_minute.grid(row=3,column=0)
            input_minute = tk.Entry(window_frame)
            input_minute.grid(row=3,column=1)

            label_second_text = "Second: "
            label_second = tk.Label(window_frame, text=label_second_text)
            label_second.grid(row=4,column=0)
            input_second = tk.Entry(window_frame)
            input_second.grid(row=4,column=1)

            submit_button = tk.Button(window_frame, text='Submit', command=submit_data)
            submit_button.grid(row=5, column=1)

        def view_model_contents_window():
            window = tk.Toplevel(master)
            window.title('View Model Contents')
            window.geometry("600x500")

            window_frame = tk.Frame(window, width=300, height=400)
            window_frame.grid(row=0,column=0)

            cluster_model_contents = generate_model.show_model_data()

            for x in range(0, len(cluster_model_contents)):
                txt = cluster_model_contents[x]
                text = tk.Label(window_frame, text=txt, wraplength=600)
                text.grid(row=x,column=0)

        def view_misc_info_window():
            def more_info():
                listbox_misc.delete(0,tk.END)
                listbox_misc.insert(0, "Total number of csv files used for training: " + str(len(generate_model.glob.glob(generate_model.path))))
                listbox_misc.insert(1, "Total number of articles used for training: " + str(len(generate_model.df)))
                listbox_misc.insert(2, "Total number of words after using stop words and vectorization: " + str(len(generate_model.word_features)))
                listbox_misc.insert(3, "Total number of words after using stop words, tokenization and vectorization : " + str(len(generate_model.word_features2)))
                listbox_misc.insert(4, "Total number of Clusters: " + str(generate_model.kmeans.n_clusters))

            def num_of_articles_per_cluster():
                k = generate_model.kmeans.n_clusters
                label_dict = []

                with open("selected_model.txt") as f:
                    text = f.read()
                    a = text.strip()
                    file_name = os.path.basename(a)
                    no_extension = os.path.splitext(file_name)[0]

                if not os.path.exists("cluster_labels/"+no_extension+".txt"):
                    with open("cluster_labels/"+no_extension+".txt",'w+') as file:
                        file.write("")
                    
                for z in range (0, k):
                    with open("cluster_labels/"+no_extension+".txt") as f:
                        text = f.read()
                        if text == '':
                            text = "{}"
                        label_dict = json.loads(text)
                
                listbox_misc.delete(0,tk.END)
                data = pd.read_csv("main_with_clusters.csv", names=colnames, encoding='latin-1', header=1)
                for x in range(0, generate_model.kmeans.n_clusters):
                    xcluster = len(data.loc[data['cluster'] == x])
                    if str(x) in label_dict:
                        listbox_misc.insert(x, "Cluster "+str(x)+" ("+label_dict[str(x)]+")"+" : " + str(xcluster) + " Article(s)")
                    else:
                        listbox_misc.insert(x, "Cluster "+str(x)+" (No Label)"+" : " + str(xcluster) + " Article(s)")

                    
            window = tk.Toplevel(master)
            window.title('View Miscellaneous Information')
            window.geometry("500x300")
        
            window_frame_listbox = tk.Frame(window, width=400, height=300)
            window_frame_listbox.pack(side='top')

            #window_frame_buttons = tk.Frame(window,bg='blue', width=400, height=200)
            #window_frame_buttons.pack(side='bottom')

            scrollbar_misc = tk.Scrollbar(window_frame_listbox)
            scrollbar_misc.pack(side=tk.RIGHT, fill="y")
            listbox_misc = tk.Listbox(window_frame_listbox, yscrollcommand=scrollbar_misc.set, width=300, height=15)
            listbox_misc.pack(side=tk.LEFT, expand=True, fill="both")
            scrollbar_misc.config(command=listbox_misc.yview)

            num_of_articles_per_cluster()
            '''reset_button = tk.Button(window_frame_buttons, text="Main Information",height=2,width=20, borderwidth=1, command=num_of_articles_per_cluster)
            reset_button.pack(side="left")
            more_button = tk.Button(window_frame_buttons, text="More Information",height=2,width=20, borderwidth=1, command=more_info)
            more_button.pack(side="left")'''
            
        def view_per_month():
            plot.show_month()
            
        def about():
            listbox.delete(0,tk.END)
            listbox.insert(0,"Authors: ")
            listbox.insert(1,"        Glenn Matthew P. Perez")
            listbox.insert(2,"        Steven Clien B. Ramos")
            listbox.insert(3,"        Angelo L. Duran")
            listbox.insert(4,"                  ")
            listbox.insert(5,"        Bicol University")
            listbox.insert(6,"        © 2019")
            
            
        # Initialize Frames
        title_frame = tk.Frame(master, height=10)
        #notification_frame = tk.Frame(master, height=60, width=550)
        category_frame = tk.Frame(master, width=290, height=230)
        listbox_frame = tk.Frame(master, width=290, height=230)
        page_frame = tk.Frame(master, height=50, width=500)

        # Set position of frames
        page_frame.pack(side='bottom')
        title_frame.pack(side='top')
        #notification_frame.pack(side='top')
        
        category_frame.pack(side='left')
        listbox_frame.pack(side='right')
        

        # Add Menu bar
        menubar = tk.Menu(master)

        # Menu Contents 
        options_menu = tk.Menu(menubar, tearoff=0)
        options_menu.add_command(label="Non-scheduled Collection", command=manual_collect_data)
        #options_menu.add_command(label="Exit", command=close_all)

        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Change Category Names", command=change_label_window)
        settings_menu.add_command(label="Change Scheduled Time", command=change_sched_time)
        settings_menu.add_command(label="Limit View per Category", command=limit_view)
        settings_menu.add_command(label="Upload Model", command=upload_model)
        #settings_menu.add_command(label="Generate Model", command=gen_model)
        #settings_menu.add_command(label="Conduct Elbow Method Test")

        stats_menu = tk.Menu(menubar, tearoff=0)
        stats_menu.add_command(label="View Model Contents", command=view_model_contents_window)
        stats_menu.add_command(label="View Plots", command=plot.pca)
        stats_menu.add_command(label="View Misc. Information", command=view_misc_info_window)
        stats_menu.add_command(label="View Monthly Collection", command=view_per_month)
        

        menubar.add_cascade(label="File", menu=options_menu)
        menubar.add_cascade(label="Information", menu=stats_menu)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        menubar.add_cascade(label="About", command=about)

        # Display the menu
        master.config(menu=menubar)

        # Display the Title
        photo = tk.PhotoImage(file="img/app_title.png")
        title_label = tk.Label(title_frame, image=photo)
        title_label.photo = photo
        title_label.pack()
        
        #Nofification Title
        #notif_label = tk.Label(notification_frame, text='Notifications:')
        #notif_label.grid(row=0,column=0)

        
        notif_dict = {}
        def notifications():
            label_dict = []
            with open("selected_model.txt") as f:
                text = f.read()
                a = text.strip()
                file_name = os.path.basename(a)
                no_extension = os.path.splitext(file_name)[0]

            if not os.path.exists("cluster_labels/"+no_extension+".txt"):
                with open("cluster_labels/"+no_extension+".txt",'w+') as file:
                    file.write("")
            
            with open("cluster_labels/"+no_extension+".txt") as f:
                text = f.read()
                if text == '':
                    text = "{}"
                label_dict = json.loads(text)
            #print(label_dict)
            with open("latest.txt", "r") as latest_:
                notif = latest_.read()
            notif_split = notif.split(',')
            notif_count = np.unique(notif_split, return_counts=True)

            #print(len(notif_split))
            for x in range(0, len(notif_count[0])):
                if notif_split[0] == '':
                    break
                if str(x) in label_dict:
                    txt = str(label_dict[notif_count[0][x]]) + ": " + str(notif_count[1][x]) + " new article(s)"
                    ntf_lbl = tk.Label(notification_frame, text=txt, foreground='green')
                    notif_dict[x] = ntf_lbl
                    ntf_lbl.grid(row=x+1,column=0)
                else:
                    txt = "No Label : " + str(notif_count[1][x]) + " new article(s)"
                    ntf_lbl = tk.Label(notification_frame, text=txt, foreground='green')
                    notif_dict[x] = ntf_lbl
                    ntf_lbl.grid(row=x+1,column=0)
                    

            if len(notif_dict) == 0:
                notif_dict[0] = tk.Label(notification_frame, text="There are no new notifications at this time...", foreground='red')
                notif_dict[0].grid(row=1,column=0)

            
        #notifications()
            


        colnames = ['cluster', 'content', 'date', 'link', 'title']
        data = pd.read_csv("main_with_clusters.csv", names=colnames, encoding='latin-1', header=1)

        def next_func(param):
            #next_+=1
            nxt = param[0]
            xcluster = param[1]
            num = param[2]

            with open ("view.txt", "r") as view_file:
                view_num = int(view_file.read())

            if view_num == 0:
                view_num = None
            
            data = pd.read_csv("main_with_clusters.csv", names=colnames, encoding='latin-1', header=0)
            #reload_data()
            xcluster = data.loc[data['cluster'] == num]
            #print(xcluster)
            listbox.delete(0,tk.END)
            if len(xcluster) == 0:
                listbox.insert(0,"There are currently no news for this category...")

            title_cluster = xcluster['title'].tolist()[nxt*2+2:][:view_num]
            title_cluster_cleaned = [re.sub(r"[ ](?=[ ])|[^-_,A-Za-z0-9 ]+", "", n) for n in title_cluster]

            link_cluster = xcluster['link'].tolist()[nxt*2+2:][:view_num]

            date_cluster = xcluster['date'].tolist()[nxt*2+2:][:view_num]

            

            for x in range(0, len(date_cluster)):
                if "/" in date_cluster[x]:
                    date_cluster[x] = datetime.datetime.strptime(date_cluster[x], '%d/%m/%Y').strftime('%Y-%m-%d')

                    
            for x in range(0,len(title_cluster)):
                dt = datetime.datetime.strptime(date_cluster[x], '%Y-%m-%d')
                month = calendar.month_name[dt.month]
                day = dt.day
                year = dt.year
                listbox.insert(x, str(month)+", "+str(day)+", "+str(year)+": "+title_cluster_cleaned[x])

            page_button[0].configure(command=partial(next_func, [nxt-1, xcluster, num]))
            page_button[1].configure(command=partial(next_func, [nxt+1, xcluster, num]))

        def prev_func(param):
            #next_+=1
            nxt = param[0]
            xcluster = param[1]
            num = param[2]

            with open ("view.txt", "r") as view_file:
                view_num = int(view_file.read())

            if view_num == 0:
                view_num = None
            
            data = pd.read_csv("main_with_clusters.csv", names=colnames, encoding='latin-1', header=0)
            #reload_data()
            xcluster = data.loc[data['cluster'] == num]
            #print(xcluster)
            listbox.delete(0,tk.END)
            if len(xcluster) == 0:
                listbox.insert(0,"There are currently no news for this category...")

            title_cluster = xcluster['title'].tolist()[nxt*2-2:][:view_num]
            title_cluster_cleaned = [re.sub(r"[ ](?=[ ])|[^-_,A-Za-z0-9 ]+", "", n) for n in title_cluster]

            link_cluster = xcluster['link'].tolist()[nxt*2-2:][:view_num]

            date_cluster = xcluster['date'].tolist()[nxt*2-2:][:view_num]

            print(nxt+nxt)            

            for x in range(0, len(date_cluster)):
                if "/" in date_cluster[x]:
                    date_cluster[x] = datetime.datetime.strptime(date_cluster[x], '%d/%m/%Y').strftime('%Y-%m-%d')

                    
            for x in range(0,len(title_cluster)):
                dt = datetime.datetime.strptime(date_cluster[x], '%Y-%m-%d')
                month = calendar.month_name[dt.month]
                day = dt.day
                year = dt.year
                listbox.insert(x, str(month)+", "+str(day)+", "+str(year)+": "+title_cluster_cleaned[x])

            page_button[0].configure(command=partial(next_func, [nxt-1, xcluster, num]))
            page_button[1].configure(command=partial(next_func, [nxt+1, xcluster, num]))
            
            

        def button_action(num):
            prev = 0
            next_ = 0
            value = 1
            if len(page_button) > 0:
                page_button[0].destroy()
                page_button[1].destroy()
            #notif_dict[num].destroy()
            #notifications()
            #reload(generate_model)
            #generate_model.main_with_clusters()
            with open ("view.txt", "r") as view_file:
                view_num = int(view_file.read())

            if view_num == 0:
                view_num = None
            
            data = pd.read_csv("main_with_clusters.csv", names=colnames, encoding='latin-1', header=0)
            #reload_data()
            xcluster = data.loc[data['cluster'] == num]
            #print(xcluster)
            listbox.delete(0,tk.END)
            if len(xcluster) == 0:
                listbox.insert(0,"There are currently no news for this category...")

            title_cluster = xcluster['title'].tolist()[:view_num]
            title_cluster_cleaned = [re.sub(r"[ ](?=[ ])|[^-_,A-Za-z0-9 ]+", "", n) for n in title_cluster]

            link_cluster = xcluster['link'].tolist()[:view_num]

            date_cluster = xcluster['date'].tolist()[:view_num]

            for x in range(0, len(date_cluster)):
                if "/" in date_cluster[x]:
                    date_cluster[x] = datetime.datetime.strptime(date_cluster[x], '%d/%m/%Y').strftime('%Y-%m-%d')

                    
            for x in range(0,len(title_cluster)):
                dt = datetime.datetime.strptime(date_cluster[x], '%Y-%m-%d')
                month = calendar.month_name[dt.month]
                day = dt.day
                year = dt.year
                listbox.insert(x, str(month)+", "+str(day)+", "+str(year)+": "+title_cluster_cleaned[x])

            def go_to_link(self):
                selection = listbox.curselection()
                sel = int(selection[0])
                webbrowser.open(link_cluster[sel])

            if view_num != None:
                page_button[0] = tk.Button(page_frame, text='Previous', borderwidth=1)
                page_button[1] = tk.Button(page_frame, text='Next', borderwidth=1, command=partial(next_func, [next_, xcluster, num]))
            
                page_button[0].pack(side='left')
                page_button[1].pack(side='left')


            listbox.bind( "<Double-Button-1>" , go_to_link)
            #print(len(category_button))
            categ_button_edit_color(num)



        def categ_button_edit_color(num):
            #s = str(s)
            category_button[num].configure(bg='gray')

            for x in range(0,len(category_button)):
                if num != x:
                    category_button[x].configure(bg='#F0F0F0')

        def categ_button_edit_text(s, num):
            s = str(s)
            category_button[num].configure(text=s)

        def notif_button_action(a):
            num = a[0]
            data = pd.read_csv("main_with_clusters.csv", names=colnames, encoding='latin-1', header=0)
            xcluster = data.loc[data['cluster'] == num][:int(a[1])]
            
            listbox.delete(0,tk.END)
            if len(xcluster) == 0:
                listbox.insert(0,"There are currently new notifications for this category...")

            title_cluster = xcluster['title'].tolist()
            title_cluster_cleaned = [re.sub(r"[ ](?=[ ])|[^-_,A-Za-z0-9 ]+", "", n) for n in title_cluster]

            link_cluster = xcluster['link'].tolist()

            date_cluster = xcluster['date'].tolist()

            for x in range(0, len(date_cluster)):
                if "/" in date_cluster[x]:
                    date_cluster[x] = datetime.datetime.strptime(date_cluster[x], '%d/%m/%Y').strftime('%Y-%m-%d')

                    
            for x in range(0,len(title_cluster)):
                dt = datetime.datetime.strptime(date_cluster[x], '%Y-%m-%d')
                month = calendar.month_name[dt.month]
                day = dt.day
                year = dt.year
                listbox.insert(x, str(month)+", "+str(day)+", "+str(year)+": "+title_cluster_cleaned[x])

            def go_to_link(self):
                selection = listbox.curselection()
                sel = int(selection[0])
                webbrowser.open(link_cluster[sel])

            listbox.bind( "<Double-Button-1>" , go_to_link)
            
            
        def create_category_buttons():
            k = generate_model.kmeans.n_clusters
            label_dict = []

            with open("selected_model.txt") as f:
                text = f.read()
                a = text.strip()
                file_name = os.path.basename(a)
                no_extension = os.path.splitext(file_name)[0]

            if not os.path.exists("cluster_labels/"+no_extension+".txt"):
                with open("cluster_labels/"+no_extension+".txt",'w+') as file:
                    file.write("")
            
            # Create Buttons
            for z in range (0, k):
                with open("cluster_labels/"+no_extension+".txt") as f:
                    text = f.read()
                    if text == '':
                        text = "{}"
                    label_dict = json.loads(text)
                    

                if (str(z) in label_dict):
                    name = label_dict[str(z)]
                    category_button[z] = tk.Button(category_frame,bg='#F0F0F0',text=name,height=2,width=20, borderwidth=1, command=partial(button_action, z))
                else:
                    category_button[z] = tk.Button(category_frame,bg='#F0F0F0',text='No Label',height=2,width=20, borderwidth=1, command=partial(button_action, z))

                with open("latest.txt", "r") as latest_:
                    notif = latest_.read()
                notif_split = notif.split(',')
                notif_count = np.unique(notif_split, return_counts=True)

                if notif_split[0] == '':
                    notif_count_ = str(0)
                else:
                    if str(z) in notif_count[0]:
                        index_notif = np.where(notif_count[0] == str(z))
                        notif_count_ = str(int(notif_count[1][index_notif]))
                    else:
                        notif_count_ = str(0)
                
                if int(notif_count_) == 0:
                    notif_button[z] = tk.Button(category_frame,text="("+notif_count_+")",height=2,width=2,state='disabled',borderwidth=0, cursor='hand2', command=partial(notif_button_action, [z,notif_count_]))
                else:
                    notif_button[z] = tk.Button(category_frame,text="("+notif_count_+")",height=2,width=2,borderwidth=0, cursor='hand2', command=partial(notif_button_action, [z,notif_count_]))
                
                category_button[z].grid(row=z,column=0)
                notif_button[z].grid(row=z,column=1)
        #print(label_dict)
                
        def refresh_category_buttons():
            for x in range(0, len(category_button)):
                category_button[x].destroy()
                notif_button[x].destroy()
            #create_category_buttons()
            
        
        create_category_buttons()

        #category_button[0].destroy()
        #button_identities[1].destroy
            
        # Listbox
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set, width=300, height=15)
        listbox.insert(0, "Welcome to the AppDated!")
        listbox.insert(1, "This application identifies topics in Bicol-related")
        listbox.insert(2, "news articles through the use of generated")
        listbox.insert(3, "clustered models.")
        listbox.pack(side=tk.LEFT, expand=True, fill="both")
        scrollbar.config(command=listbox.yview)



        t1 = Thread(target=collect_data_scheduled) # Initialize Thread
        t1.start() # Start Thread     
          
def on_close():
    os._exit(1)
        
def start_gui():
    root = tk.Tk()
    root.title("Appdated: An Application Categorizing Bicol Related News Articles")
    #root.iconbitmap('img/favicon.ico')
    root.geometry("700x550")
    app = Application(root)
    root.protocol("WM_DELETE_WINDOW",  on_close)
    root.mainloop()    

if __name__ == '__main__':
    start_gui()
