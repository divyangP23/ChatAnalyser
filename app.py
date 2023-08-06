from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import Image , ImageTk
from tkinter import filedialog
from tkinter import messagebox
import numpy as np
import pandas as pd
import re
from datetime import datetime
from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
from tkinter import Scrollbar
import emoji
import plotly.express as px
from pandas.api.types import CategoricalDtype
import seaborn as sns


f=open('Hinglish_stopwords.txt','r')
stop_words = f.read()

# Define the custom order of days
custom_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Create a Categorical data type with the custom order
cat_dtype = CategoricalDtype(categories=custom_order, ordered=True)

class WPChatAnalyse:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1920x1080+0+0")
        self.root.title("WhatsApp Chat Analyser")

        # placing bg image
        img_bg = Image.open(
            r"background_image.jpg")
        img_bg = img_bg.resize((1920, 1080), Image.ANTIALIAS)
        self.photoimg_bg = ImageTk.PhotoImage(img_bg)
        bg_lbl = Label(self.root, image=self.photoimg_bg)
        bg_lbl.place(x=0, y=0, width=1920, height=1080)

        # placing text above the bg image
        title_lbl = Label(bg_lbl, text="WHATSAPP CHAT ANALYSER", font=("Assassin$", 50, "bold"), fg="yellow",bg="black")
        title_lbl.place(x=0, y=0, width=1920, height=65)

        main_frame = Frame(bg_lbl, bd=3, bg="green")
        main_frame.place(x=10, y=75, width=1900, height=915)

        self.left_frame = Frame(main_frame,bd=3,bg="pink")
        self.left_frame.place(x=2,y=2,width=530,height=903)

        self.right_frame = Frame(main_frame,bd=3,bg="purple")
        self.right_frame.place(x=544,y=2,width=1344,height=903)



        text_lbl1 = Label(self.left_frame,text="1) Go to the chat you want to export.",bg="pink",wraplength=520,font=("Rancho", 20, "bold"),justify=LEFT)
        text_lbl1.place(x=5,y=15)
        text_lbl2 = Label(self.left_frame,text="2)Tap on the contact or group name at the top of the screen to open the contact/group info.",bg="pink",wraplength=520,font=("Rancho", 20, "bold"),justify=LEFT)
        text_lbl2.place(x=5,y=55)
        text_lbl3 = Label(self.left_frame,text="3)Within the contact/group info, look for the option 'Export Chat' or 'Chat Export' (the exact wording may vary depending on your device).",bg="pink",wraplength=520,font=("Rancho", 20, "bold"),justify=LEFT)
        text_lbl3.place(x=5,y=95)
        text_lbl4 = Label(self.left_frame,text="4)Tap on the 'Export Chat' option.",bg="pink",wraplength=520,font=("Rancho", 20, "bold"),justify=LEFT)
        text_lbl4.place(x=5,y=200)
        text_lbl4 = Label(self.left_frame,text="5)You will be presented with two options: 'Attach Media' and 'Without Media'. Select option 'Without Media'",bg="pink",wraplength=520,font=("Rancho", 20, "bold"),justify=LEFT)
        text_lbl4.place(x=5,y=240)
        text_lbl5 = Label(self.left_frame, text="6)Save this file in .txt format. ", bg="pink", wraplength=520,font=("Rancho", 20, "bold"), justify=LEFT)
        text_lbl5.place(x=5, y=345)


        self.upload_button = Button(self.left_frame, text="Upload File", command=self.upload_file,font=("Rancho", 25, "bold"),fg="red",bg="yellow")
        self.upload_button.place(x=150,y=400,width=200)


    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

        # Check if a file was selected
        if file_path:
            # Open the file in read mode with UTF-8 encoding
            with open(file_path, 'r', encoding='utf-8') as file:
                data = file.read()
                data = data.replace('\u202f', ' ')
                print(data)



        # print("Selected file:", file_path)
        self.text_lbl5 = Label(self.left_frame, text="Selected File: ", bg="pink", wraplength=520,font=("Rancho", 20, "bold"), justify=LEFT,fg="green")
        self.text_lbl5.place(x=2, y=395)
        self.text_lbl6 = Label(self.left_frame, text="", bg="pink", wraplength=520,font=("Rancho", 20, "bold"), justify=LEFT,fg="purple")
        self.text_lbl6.place(x=2, y=425)
        self.text_lbl6.config(text=file_path)
        self.upload_button.destroy()


        self.text_lbl6 = Label(self.left_frame, text="Analyse wrt. ", bg="pink", wraplength=520,font=("Rancho", 30, "bold"), justify=LEFT,fg="purple")
        self.text_lbl6.place(x=5, y=595)



        self.analyse_button = Button(self.left_frame, text="Analyse",font=("Rancho", 25, "bold"), fg="red", bg="yellow",command=self.analyse)
        self.analyse_button.place(x=150, y=720, width=200)

        pattern_messages = r'\d{1,2}/\d{1,2}/\d{1,2}, \d{1,2}:\d{2}\s[AP]M - (.+)'
        messages = re.findall(pattern_messages, data)

        formatted_messages = ["" + message + "" for message in messages]

        # Assuming 'data' contains the text from the WhatsApp chat
        messages_date_time = re.findall(r'(\d{1,2}/\d{1,2}/\d{2}), (\d{1,2}:\d{2} [AP]M)', data)

        # Extract the date, time, and message components
        formatted_messages_date = []
        for message_date in messages_date_time:
            date = message_date[0]
            formatted_message_date = f'{date}'
            formatted_messages_date.append(formatted_message_date)

        formatted_messages_time = []
        for message_time in messages_date_time:
            time = message_time[1]
            formatted_message_time = f'{time}'
            formatted_messages_time.append(formatted_message_time)

        # print(len(formatted_messages_time),len(formatted_messages_date))

        self.table = pd.DataFrame(
            {'user_message': formatted_messages, 'date': formatted_messages_date, 'time': formatted_messages_time})
        users = []
        messages = []
        for message in self.table['user_message']:
            entry = re.split('([\w\W]+?):\s', message)
            if entry[1:]:
                users.append(entry[1])
                messages.append(entry[2])
            else:
                users.append("Group Notification")
                messages.append(entry[0])

        self.table['user'] = users
        self.table['message'] = messages
        self.table.drop(columns=['user_message'], inplace=True)
        self.table = self.table.dropna()
        self.table['date'] = pd.to_datetime(self.table['date'], format='%m/%d/%y')
        self.table['day'] = self.table['date'].dt.strftime('%d')
        self.table['month'] = self.table['date'].dt.strftime('%m')
        self.table['year'] = self.table['date'].dt.year
        self.table.drop(columns=['date'], inplace=True)
        self.table['time'] = pd.to_datetime(self.table['time'], format='%I:%M %p')
        self.table['hour'] = self.table['time'].dt.strftime('%I')
        self.table['minute'] = self.table['time'].dt.strftime('%M')
        self.table['period'] = self.table['time'].dt.strftime('%p')
        self.table.drop(columns=['time'], inplace=True)
        self.table = self.table.rename(columns={'day': 'date'})


        # print(self.table)
        valid_users = self.table['user'].unique().tolist()
        valid_users.remove('Group Notification')
        valid_users.sort()
        valid_users.insert(0, 'Overall')
        # print(valid_users)

        self.user_value_lbl = ttk.Combobox(self.left_frame, width=30, font=("Rancho", 20, "bold"), state="readonly")
        self.user_value_lbl["values"] = valid_users
        self.user_value_lbl.current(0)
        self.user_value_lbl.place(x=5,y=645)

    def analyse(self):

        self.first_frame = Frame(self.right_frame, bd=3, bg="orange")
        self.first_frame.place(x=5, y=5, width=1333)

        head_1 = Label(self.first_frame, text="Total Messages", font=("Rancho", 30, "bold"), fg="Black", bg="orange")
        head_1.grid(row=0, column=0, sticky=NSEW, padx=5, pady=5)

        head_2 = Label(self.first_frame, text="Total Words", font=("Rancho", 30, "bold"), fg="Black", bg="orange")
        head_2.grid(row=0, column=1, sticky=NSEW, padx=5, pady=5)

        head_3 = Label(self.first_frame, text="Total Media\n Shared", font=("Rancho", 30, "bold"), fg="Black",
                       bg="orange")
        head_3.grid(row=0, column=2, sticky=NSEW, padx=5, pady=5)

        head_4 = Label(self.first_frame, text="Total Links\n Shared", font=("Rancho", 30, "bold"), fg="Black",
                       bg="orange")
        head_4.grid(row=0, column=3, sticky=NSEW, padx=5, pady=5)

        head_5 = Label(self.first_frame, text="Busiest Person", font=("Rancho", 30, "bold"), fg="Black",
                       bg="orange")
        head_5.grid(row=0, column=4, sticky=NSEW, padx=5, pady=5)

        self.second_frame = Frame(self.right_frame, bd=3, bg="green")
        self.second_frame.place(x=5, y=200, width=1333, height=670)
        canvas = Canvas(self.second_frame)
        scrollbar = Scrollbar(self.second_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.configure(scrollregion=canvas.bbox("all"))

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")



        df = self.table
        user_df = self.table[self.table['user']==self.user_value_lbl.get()]

        if self.user_value_lbl.get()=="Overall":

            self.head_value_1 = Label(self.first_frame,text=df.shape[0],font=("Rancho", 30, "bold"),fg="Black",bg="orange")
            self.head_value_1.grid(row=1,column=0,sticky=NSEW,padx=5,pady=5)

            words = []
            for i in df['message']:
                words.extend(i.split())

            self.head_value_2 = Label(self.first_frame,text=len(words),font=("Rancho", 30, "bold"),fg="Black",bg="orange")
            self.head_value_2.grid(row=1,column=1,sticky=NSEW,padx=5,pady=5)

            media_df = df[df['message'] == "<Media omitted>"]

            self.head_value_3 = Label(self.first_frame,text=media_df.shape[0],font=("Rancho", 30, "bold"),fg="Black",bg="orange")
            self.head_value_3.grid(row=1,column=2,sticky=NSEW,padx=5,pady=5)

            links = []
            extractor = URLExtract()
            for i in df['message']:
                links.extend(extractor.find_urls(i))

            self.head_value_4 = Label(self.first_frame, text=len(links), font=("Rancho", 30, "bold"), fg="Black",
                                      bg="orange")
            self.head_value_4.grid(row=1, column=3, sticky=NSEW, padx=5, pady=5)


            user_count = df['user'].value_counts().drop('Group Notification')
            max_user = user_count.idxmax()

            self.head_value_5 = Label(self.first_frame, text=max_user, font=("Rancho", 30, "bold"), fg="Black",
                                      bg="orange")
            self.head_value_5.grid(row=1, column=4, sticky=NSEW, padx=5, pady=5)


            x_df = df['user'].value_counts().drop('Group Notification')
            x=x_df.head()
            name = x.index
            count = x.values
            plt.bar(name, count, color="purple")
            plt.title("Top Busy Users")
            plt.ylabel('Messages')
            plt.xlabel('User')
            plt.xticks(rotation='vertical')
            # plt.figure(figsize=(500, 500))
            plt.subplots_adjust(bottom=0.2)
            plt.savefig('plot.png', bbox_inches='tight')
            plt.close()
            side_img_plt = Image.open('plot.png')
            side_img_plt = side_img_plt.resize((500, 500), Image.ANTIALIAS)
            self.photoimg_side_plt = ImageTk.PhotoImage(side_img_plt)

            side_lbl_plt = Label(scrollable_frame, image=self.photoimg_side_plt)
            side_lbl_plt.grid(row=0,column=0, sticky=NSEW, padx=(50,30), pady=5)

            new_x = x_df.reset_index()
            # print(new_x)
            total=new_x['count'].sum()
            # print(total)
            percent=round((new_x['count']/total)*100,2)
            # print(percent)
            new_x["Message Percentage"]=percent
            new_x = new_x.drop(columns=['count'])
            new_x=new_x.head(10)
            # print(new_x)

            fig,ax=plt.subplots()
            ax.axis('off')

            display = ax.table(cellText = new_x.values,colLabels = new_x.columns,loc = 'upper center')

            display.auto_set_font_size(False)
            display.set_fontsize(15)
            display.scale(1.5,1.8)
            plt.title("Top 10 Frequent Users",y=1.1)

            # print(plt.show())
            plt.savefig('plot_2.png', bbox_inches='tight')
            plt.close()
            side_img_plt_2 = Image.open('plot_2.png')
            side_img_plt_2 = side_img_plt_2.resize((700, 500), Image.ANTIALIAS)
            self.photoimg_side_plt_2 = ImageTk.PhotoImage(side_img_plt_2)

            side_lbl_plt_2 = Label(scrollable_frame, image=self.photoimg_side_plt_2)
            side_lbl_plt_2.grid(row=0,column=1, sticky=NSEW, padx=(10,20), pady=5)

            temp = df[df['user']!='Group Notification']
            temp = temp[temp['message']!='<Media omitted>']

            # Create an instance of WordCloud
            wc = WordCloud(background_color="white", width=500, height=500, min_font_size=10)

            messages = ' '.join(temp['message'].astype(str))

            # Generate the word cloud
            wc.generate(messages)

            # Display the word cloud
            plt.imshow(wc, interpolation="bilinear")
            plt.axis("off")
            # plt.show()
            plt.title("Word Cloud",pad=15)

            # print(plt.show())
            plt.savefig('plot_3.png', bbox_inches='tight')
            plt.close()
            side_img_plt_3 = Image.open('plot_3.png')
            side_img_plt_3 = side_img_plt_3.resize((500, 500), Image.ANTIALIAS)
            self.photoimg_side_plt_3 = ImageTk.PhotoImage(side_img_plt_3)


            side_lbl_plt_3 = Label(scrollable_frame, image=self.photoimg_side_plt_3)
            side_lbl_plt_3.grid(row=1, column=0, sticky=NSEW, padx=(50, 30), pady=15)


            # Convert the DataFrame column to a string

            f = open('Hinglish_stopwords.txt', 'r')
            stop_words = f.read()
            words = []
            for message in temp['message']:
                for word in message.lower().split():
                    if word not in stop_words:
                        words.append(word)
            top_words = pd.DataFrame(Counter(words).most_common(20))
            x = top_words[0]
            y = top_words[1]

            # Create the line graph
            plt.plot(x, y, marker='o', linestyle='-', color='b')

            # Add labels and title
            plt.xlabel('Words')
            plt.ylabel('Frequency')
            plt.xticks(rotation='vertical')
            plt.title('Frequently Used Words')

            # Display the graph
            # plt.show()

            plt.savefig('plot_5.png', bbox_inches='tight')
            plt.close()
            side_img_plt_5 = Image.open('plot_5.png')
            side_img_plt_5 = side_img_plt_5.resize((700, 500), Image.ANTIALIAS)
            self.photoimg_side_plt_5 = ImageTk.PhotoImage(side_img_plt_5)

            side_lbl_plt_5 = Label(scrollable_frame, image=self.photoimg_side_plt_5)
            side_lbl_plt_5.grid(row=1, column=1, sticky=NSEW, padx=(10,20), pady=5)

            emojis = []
            for message in temp['message']:
                emojis.extend([c for c in message if emoji.is_emoji(c)])
            emojis_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
            emojis_df=emojis_df.head(7)
            # print(emojis_df)
            # Switch to the TkAgg backend
            # Switch to the TkAgg backend
            plt.switch_backend('TkAgg')

            # Create a pie chart using plotly
            fig = px.pie(emojis_df, names=0, values=1)

            # Set the title
            fig.update_layout(title_text='Top Emojis')

            # Display the chart
            # fig.show()
            # Save the figure as a PNG image
            fig.write_image("emoji_pie_chart.png", engine="kaleido",width=500,height=500)
            side_img_plt_6 = Image.open('emoji_pie_chart.png')
            side_img_plt_6 = side_img_plt_6.resize((500, 500), Image.ANTIALIAS)
            self.photoimg_side_plt_6 = ImageTk.PhotoImage(side_img_plt_6)

            side_lbl_plt_6 = Label(scrollable_frame, image=self.photoimg_side_plt_6)
            side_lbl_plt_6.grid(row=2, column=0, sticky=NSEW, padx=(50, 30), pady=15)

            timeline_df =df.groupby(['year', 'month']).count()['message'].reset_index()
            time = []
            for i in range(timeline_df.shape[0]):
                time.append(timeline_df['month'][i] + "/" + str(timeline_df['year'][i]))
            timeline_df['time'] = time
            # print(timeline_df['time'])
            months = timeline_df['time']
            values_month = timeline_df['message']
            plt.plot(months, values_month, marker='o',color="orange")

            plt.xlabel("Months")
            plt.ylabel("Messages Sent")
            plt.title("Monthly Analysis")
            plt.grid(True)
            plt.xticks(rotation=45)  # Rotates x-axis labels for better readability

            # plt.show()
            plt.savefig('plot_7.png', bbox_inches='tight')
            plt.close()
            side_img_plt_7 = Image.open('plot_7.png')
            side_img_plt_7 = side_img_plt_7.resize((700, 500), Image.ANTIALIAS)
            self.photoimg_side_plt_7 = ImageTk.PhotoImage(side_img_plt_7)

            side_lbl_plt_7 = Label(scrollable_frame, image=self.photoimg_side_plt_7)
            side_lbl_plt_7.grid(row=2, column=1, sticky=NSEW, padx=(10,20), pady=5)

            timeline_day_df = df.groupby(['year', 'month', 'date']).count()['message'].reset_index()
            time_day = []
            for i in range(timeline_day_df.shape[0]):
                time_day.append(
                    timeline_day_df['date'][i] + "/" + timeline_day_df['month'][i] + "/" + str(timeline_day_df['year'][i]))
            timeline_day_df['time_day'] = time_day
            # print(timeline_day_df)

            dates = timeline_day_df['time_day']
            values_dates = timeline_day_df['message']
            plt.plot(dates, values_dates, marker='o',color="purple")

            plt.xlabel("Dates")
            plt.ylabel("Messages Sent")
            plt.title("Daily Analysis")
            plt.grid(False)
            plt.xticks(rotation='vertical')  # Rotates x-axis labels for better readability
            # plt.figure(figsize=(12, 6))
            # plt.show()
            plt.savefig('plot_9.png', bbox_inches='tight')
            plt.close()
            side_img_plt_9 = Image.open('plot_9.png')
            side_img_plt_9 = side_img_plt_9.resize((500, 500), Image.ANTIALIAS)
            self.photoimg_side_plt_9 = ImageTk.PhotoImage(side_img_plt_9)
            side_lbl_plt_9 = Label(scrollable_frame, image=self.photoimg_side_plt_9)
            side_lbl_plt_9.grid(row=3, column=0, sticky=NSEW, padx=(50, 30), pady=15)


            day_df = pd.to_datetime(timeline_day_df['time_day'], format='%d/%m/%Y')
            timeline_day_df['day'] = day_df.dt.day_name()
            message_counts = timeline_day_df.groupby('day')['message'].sum()
            day_msg = message_counts.reset_index()
            # Assign the Categorical data type to the 'day' column
            day_msg['day'] = day_msg['day'].astype(cat_dtype)

            # Sort the DataFrame based on the custom order
            sorted_day_msg = day_msg.sort_values('day')


            name = sorted_day_msg['day']
            count = sorted_day_msg['message']
            plt.bar(name, count, color="green")
            plt.title("Day Wise Analysis")
            plt.ylabel('Messages')
            plt.xlabel('Day')
            plt.xticks(rotation='vertical')
            # plt.figure(figsize=(500, 500))
            plt.subplots_adjust(bottom=0.2)
            plt.savefig('plot_11.png', bbox_inches='tight')
            plt.close()
            side_img_plt_11 = Image.open('plot_11.png')
            side_img_plt_11 = side_img_plt_11.resize((700, 500), Image.ANTIALIAS)
            self.photoimg_side_plt_11 = ImageTk.PhotoImage(side_img_plt_11)

            side_lbl_plt_11 = Label(scrollable_frame, image=self.photoimg_side_plt_11)
            side_lbl_plt_11.grid(row=3, column=1,  sticky=NSEW, padx=(10,20), pady=5)

            final_day = []
            for i in range(df.shape[0]):
                final_day.append(df['date'][i] + "/" + df['month'][i] + "/" + str(df['year'][i]))
            df['final_date'] = final_day
            final_day_df = pd.to_datetime(df['final_date'], format='%d/%m/%Y')
            df['final_day'] = final_day_df.dt.day_name()
            hist_df = df.groupby(['hour', 'period', 'final_day', 'final_date']).count()['message'].reset_index()
            hour_span = []
            for i in range(hist_df.shape[0]):
                hour_span.append(hist_df['hour'][i] + " " + hist_df['period'][i])
            hist_df['hour_span'] = hour_span
            hist_df['hour_span'] = pd.to_datetime(hist_df['hour_span'], format='%I %p').dt.strftime('%H:%M')
            hour_span = []
            for i in range(hist_df.shape[0]):
                x = hist_df['hour_span'][i]
                #     for j in range(len(x)):
                #         hour_span.append(x[j])
                hour_span.append(x[0:2])
            hist_df['hour_span'] = hour_span
            gap = []
            for i in range(hist_df.shape[0]):
                x = hist_df['hour_span'][i]
                if x == '23':
                    gap.append(0)
                else:
                    gap.append(int(x) + 1)
            new_list = []

            for num in gap:
                new_list.append(f"{num:02}")

            hist_df['hour_span_1'] = new_list
            joined_column = [hour_span + '-' + new_list for hour_span, new_list in zip(hour_span, new_list)]
            hist_df['final_span'] = joined_column

            sns.heatmap(hist_df.pivot_table(index="final_day", columns="final_span", values="message", aggfunc='count').fillna(0))
            plt.yticks(rotation='horizontal')
            plt.xlabel("Hour-Span")
            plt.ylabel("Day")
            plt.title("Hour-Day Wise Analysis")
            # plt.show()
            plt.savefig('plot_13.png', bbox_inches='tight')
            plt.close()

            heatmap_frame = Frame(scrollable_frame,bd=3,bg="white")
            heatmap_frame.grid(row=4,rowspan=900,columnspan=900,pady=15,padx=50)
            side_img_plt_13 = Image.open('plot_13.png')
            side_img_plt_13 = side_img_plt_13.resize((1000, 600), Image.ANTIALIAS)
            self.photoimg_side_plt_13 = ImageTk.PhotoImage(side_img_plt_13)

            side_lbl_plt_13 = Label(heatmap_frame, image=self.photoimg_side_plt_13)
            side_lbl_plt_13.grid(row=4, column=0, sticky=NSEW, padx=(50, 30), pady=15)

        else:
            # self.first_frame.destroy()
            msg_user = user_df.shape[0]
            self.head_value_1.config(text=msg_user)

            user_words = []
            for i in user_df['message']:
                user_words.extend(i.split())

            self.head_value_2.config(text=len(user_words))

            user_media = user_df[user_df['message'] == "<Media omitted>"]

            self.head_value_3.config(text=user_media.shape[0])

            user_links = []
            user_extractor = URLExtract()
            for i in user_df['message']:
                user_links.extend(user_extractor.find_urls(i))

            self.head_value_4.config(text=len(user_links))

            self.head_value_5.config(text="")

            temp_user = user_df[user_df['user'] != 'Group Notification']
            temp_user = temp_user[temp_user['message'] != '<Media omitted>']

            # Create an instance of WordCloud
            wc_user = WordCloud(background_color="white", width=500, height=500, min_font_size=10)

            # Convert the DataFrame column to a string
            messages_user = ' '.join(temp_user['message'].astype(str))

            # Generate the word cloud
            wc_user.generate(messages_user)

            # Display the word cloud
            plt.imshow(wc_user, interpolation="bilinear")
            plt.axis("off")
            # plt.show()
            plt.title("Word Cloud", pad=15)

            # print(plt.show())
            plt.savefig('plot_4.png', bbox_inches='tight')
            plt.close()
            side_img_plt_user_1 = Image.open('plot_4.png')
            side_img_plt_user_1 = side_img_plt_user_1.resize((500, 500), Image.ANTIALIAS)
            self.photoimg_side_plt_user_1 = ImageTk.PhotoImage(side_img_plt_user_1)

            side_lbl_plt_user_1 = Label(scrollable_frame, image=self.photoimg_side_plt_user_1)
            side_lbl_plt_user_1.grid(row=0, column=0, sticky=NSEW, padx=(50, 30), pady=15)


            # Convert the DataFrame column to a string

            f = open('Hinglish_stopwords.txt', 'r')
            stop_words = f.read()
            words_user = []
            for message in temp_user['message']:
                for word in message.lower().split():
                    if word not in stop_words:
                        words_user.append(word)
            top_words_user = pd.DataFrame(Counter(words_user).most_common(20))
            x = top_words_user[0]
            y = top_words_user[1]

            # Create the line graph
            plt.plot(x, y, marker='o', linestyle='-', color='b')

            # Add labels and title
            plt.xlabel('Words')
            plt.ylabel('Frequency')
            plt.xticks(rotation='vertical')
            plt.title('Frequently Used Words')

            # Display the graph
            # plt.show()
            plt.savefig('plot_6.png', bbox_inches='tight')
            plt.close()
            side_img_plt_user_2 = Image.open('plot_6.png')
            side_img_plt_user_2 = side_img_plt_user_2.resize((700, 500), Image.ANTIALIAS)
            self.photoimg_side_plt_user_2 = ImageTk.PhotoImage(side_img_plt_user_2)

            side_lbl_plt_user_2 = Label(scrollable_frame, image=self.photoimg_side_plt_user_2)
            side_lbl_plt_user_2.grid(row=0, column=1, sticky=NSEW, padx=(10,20), pady=5)

            emojis_user = []
            for message in temp_user['message']:
                emojis_user.extend([c for c in message if emoji.is_emoji(c)])
            emojis_user_df = pd.DataFrame(Counter(emojis_user).most_common(len(Counter(emojis_user))))
            emojis_user_df=emojis_user_df.head(7)
            # print(emojis_user_df)
            # Switch to the TkAgg backend
            # Switch to the TkAgg backend
            plt.switch_backend('TkAgg')

            # Create a pie chart using plotly
            fig = px.pie(emojis_user_df, names=0, values=1)

            # Set the title
            fig.update_layout(title_text='Top Emojis')

            # Display the chart
            # fig.show()
            # Save the figure as a PNG image
            fig.write_image("emoji_pie_chart_user.png", engine="kaleido", width=500, height=500)
            side_img_user_3 = Image.open('emoji_pie_chart_user.png')
            side_img_user_3 = side_img_user_3.resize((500, 500), Image.ANTIALIAS)
            self.photoimg_side_user_3 = ImageTk.PhotoImage(side_img_user_3)

            side_lbl_user_3 = Label(scrollable_frame, image=self.photoimg_side_user_3)
            side_lbl_user_3.grid(row=1, column=0, sticky=NSEW, padx=(50, 30), pady=15)

            timeline_user_df =user_df.groupby(['year', 'month']).count()['message'].reset_index()
            time = []
            for i in range(timeline_user_df.shape[0]):
                time.append(timeline_user_df['month'][i] + "/" + str(timeline_user_df['year'][i]))
            timeline_user_df['time'] = time
            # print(timeline_df['time'])
            months = timeline_user_df['time']
            values_month = timeline_user_df['message']
            plt.plot(months, values_month, marker='o',color="orange")


            plt.xlabel("Months")
            plt.ylabel("Messages Sent")
            plt.title("Monthly Analysis")
            plt.grid(True)
            plt.xticks(rotation=45)  # Rotates x-axis labels for better readability

            # plt.show()
            plt.savefig('plot_8.png', bbox_inches='tight')
            plt.close()
            side_img_user_4 = Image.open('plot_8.png')
            side_img_user_4 = side_img_user_4.resize((700, 500), Image.ANTIALIAS)
            self.photoimg_side_user_4 = ImageTk.PhotoImage(side_img_user_4)

            side_lbl_user_4 = Label(scrollable_frame, image=self.photoimg_side_user_4)
            side_lbl_user_4.grid(row=1, column=1, sticky=NSEW, padx=(10,20), pady=5)

            timeline_day_user_df = user_df.groupby(['year', 'month', 'date']).count()['message'].reset_index()
            time_day_user = []
            for i in range(timeline_day_user_df.shape[0]):
                time_day_user.append(
                    timeline_day_user_df['date'][i] + "/" + timeline_day_user_df['month'][i] + "/" + str(
                        timeline_day_user_df['year'][i]))
            timeline_day_user_df['time_day'] = time_day_user
            # print(timeline_day_df)

            dates = timeline_day_user_df['time_day']
            values_dates = timeline_day_user_df['message']
            plt.plot(dates, values_dates, marker='o', color="purple")

            plt.xlabel("Dates")
            plt.ylabel("Messages Sent")
            plt.title("Daily Analysis")
            plt.grid(False)
            plt.xticks(rotation='vertical')  # Rotates x-axis labels for better readability
            # plt.figure(figsize=(12, 6))
            # plt.show()
            plt.savefig('plot_10.png', bbox_inches='tight')
            plt.close()
            side_img_user_5 = Image.open('plot_10.png')
            side_img_user_5 = side_img_user_5.resize((500, 500), Image.ANTIALIAS)
            self.photoimg_side_user_5 = ImageTk.PhotoImage(side_img_user_5)
            side_lbl_user_5 = Label(scrollable_frame, image=self.photoimg_side_user_5)
            side_lbl_user_5.grid(row=2, column=0, sticky=NSEW, padx=(50, 30), pady=15)

            day__user_df = pd.to_datetime(timeline_day_user_df['time_day'], format='%d/%m/%Y')
            timeline_day_user_df['day'] = day__user_df.dt.day_name()
            message_counts = timeline_day_user_df.groupby('day')['message'].sum()
            day_msg_user = message_counts.reset_index()
            # Assign the Categorical data type to the 'day' column
            day_msg_user['day'] = day_msg_user['day'].astype(cat_dtype)

            # Sort the DataFrame based on the custom order
            sorted_day_msg_user = day_msg_user.sort_values('day')

            name = sorted_day_msg_user['day']
            count = sorted_day_msg_user['message']
            plt.bar(name, count, color="green")
            plt.title("Day Wise Analysis")
            plt.ylabel('Messages')
            plt.xlabel('Day')
            plt.xticks(rotation='vertical')
            # plt.figure(figsize=(500, 500))
            plt.subplots_adjust(bottom=0.2)
            plt.savefig('plot_12.png', bbox_inches='tight')
            plt.close()
            side_img_user_6 = Image.open('plot_12.png')
            side_img_user_6 = side_img_user_6.resize((700, 500), Image.ANTIALIAS)
            self.photoimg_side_user_6 = ImageTk.PhotoImage(side_img_user_6)

            side_lbl_user_6 = Label(scrollable_frame, image=self.photoimg_side_user_6)
            side_lbl_user_6.grid(row=2, column=1, sticky=NSEW, padx=(10, 20), pady=5)





if __name__=="__main__":
    root = Tk()
    obj = WPChatAnalyse(root)
    root.mainloop()
